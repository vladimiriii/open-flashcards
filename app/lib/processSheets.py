# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
from datetime import datetime
from flask import session

from apiclient.discovery import build
from sqlalchemy import update

import httplib2
from oauth2client import client

from app.lib.models import Base, sheet, view, app_user_rel_sheet, db_session

###############################################
# Functions                                   #
###############################################

def get_user_sheets():

    # Query database
    user_query = ("SELECT s_id, s_google_id, s_sheet_name, s_row_count, views, s_last_modified "
                 "FROM sheet AS s "
                 "INNER JOIN ("
                    "SELECT v_s_id, COUNT(v_id) AS views "
                    "FROM public.view "
                    "WHERE v_au_id = \'" + str(session['au_id']) + "\' "
                    "GROUP BY v_s_id "
                    "ORDER BY views DESC"
                    ") AS vs "
                 "ON s.s_id = vs.v_s_id;")
    user_data = db_session.execute(user_query)

    # Process Results
    file_list = []
    for row in user_data:
        file_list.append({
            'id': row[0],
            'google_id': row[1],
            'sheet_name': row[2],
            'row_count': row[3],
            'views': row[4],
            'modified': row[5],
            })

    return file_list


def get_public_sheets():

    # Query database
    public_query = ("SELECT s_id, s_google_id, s_sheet_name, s_row_count, views, s_last_modified "
                 "FROM sheet AS s "
                 "INNER JOIN ("
                    "SELECT v_s_id, COUNT(v_id) AS views "
                    "FROM public.view "
                    "GROUP BY v_s_id "
                    "ORDER BY views DESC"
                    ") AS vs "
                 "ON s.s_id = vs.v_s_id "
                 "WHERE s_shared = TRUE;")
    public_data = db_session.execute(public_query)

    # Process Results
    file_list = []
    for row in public_data:
        file_list.append({
            'id': row[0],
            'google_id': row[1],
            'sheet_name': row[2],
            'row_count': row[3],
            'views': row[4],
            'modified': row[5],
            })

    return file_list


def get_full_list():
    # Get a list of all Sheets in the account for the current user.
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(http=httplib2.Http())
    service = build('drive', 'v3', http=http)
    response = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name, modifiedTime)').execute()

    # Get list of already imported sheet ids
    sheet_query = ("SELECT s_google_id "
                   "FROM sheet "
                   "INNER JOIN app_user_rel_sheet "
                   "ON s_id = aurs_s_id "
                   "WHERE aurs_au_id = " + str(session['au_id']))

    imported_sheets = db_session.execute(sheet_query)
    id_list = []
    for g_id in imported_sheets:
        id_list.append(g_id[0])

    # Extract Full List of Sheets, excluding those already imported
    file_list = []
    for sheet in response.get('files', []):
        # Process change
        if sheet.get('id') not in id_list:
            file_list.append({
                'name': sheet.get('name'),
                'id': sheet.get('id'),
                'modified': sheet.get('modifiedTime')
                })

    return file_list


def get_sheet_meta(g_id):
    # Get a list of all Sheets in the account for the current user.
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(http=httplib2.Http())
    service = build('drive', 'v2', http=http)
    response = service.files().get(fileId=g_id, fields='title, modifiedDate, userPermission').execute()

    meta_data = {}
    for key in response:
        meta_data[key] = response[key]

    return meta_data


def get_sheet_rows(g_id):
    # Get sheet row count
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    rangeName = 'A1:Z'
    result = service.spreadsheets().values().get(spreadsheetId=g_id, range=rangeName).execute()

    return len(result.get('values', []))

def get_owner_status(permissions):
    print(permissions)
    if permissions['role'] == 'owner':
        result = True
    else:
        result = False

    return result

def import_sheet_data(google_id):
    # Get sheet metadata
    meta_data = get_sheet_meta(google_id)
    sheet_name = meta_data['title']
    last_modified = meta_data['modifiedDate']
    row_count = get_sheet_rows(google_id)
    owner_status = get_owner_status(meta_data['userPermission'])

    # Look for existing record in sheet table
    current_sheet = sheet.query.filter_by(s_google_id = google_id).first()

    if current_sheet is None:
        # If sheet record does not yet exist, create it
        sheet_record = sheet(
                        s_ca_id = None,
                        s_sca_id = None,
                        s_google_id = google_id,
                        s_sheet_name = sheet_name,
                        s_row_count = row_count,
                        s_last_modified = last_modified,
                        s_shared = False,
                        s_date_shared = None,
                        s_hide_sharer = True)
        db_session.add(sheet_record)
        db_session.flush()
        s_id = sheet_record.s_id

        # Add Record to User Sheet Rel Table
        rel_record = app_user_rel_sheet(
                        aurs_au_id = session['au_id'],
                        aurs_s_id = s_id,
                        aurs_first_view = datetime.now(),
                        aurs_is_owner = owner_status,
                        aurs_deleted = False)

        # Update View Table
        view_record = view(
                        v_au_id = session['au_id'],
                        v_s_id = s_id,
                        v_date = datetime.now())

        # Save to Database
        db_session.bulk_save_objects([rel_record, view_record])
        db_session.commit()
        return s_id

    else:
        # Get Sheet ID
        s_id = current_sheet.s_id

        # Update View Table
        view_record = view(v_au_id = session['au_id'],
                    v_s_id = s_id,
                    v_date = datetime.now())

        # Save to Database
        db_session.add(view_record)
        db_session.commit()
        return s_id


def save_sheet_info(sheet_id, google_id):
    # Get latest sheet meta data
    meta_data = get_sheet_meta(google_id)
    sheet_name = meta_data['title']
    last_modified = meta_data['modifiedDate']
    row_count = get_sheet_rows(google_id)
    owner_status = get_owner_status(meta_data['userPermission'])

    # Update sheet record with latest metadata
    sheet_record = sheet.query.filter_by(s_id=sheet_id).first()
    sheet_record.s_sheet_name = sheet_name
    sheet_record.s_row_count = row_count
    sheet_record.s_last_modified = last_modified

    # Add new record to view table
    view_record = view(v_au_id = session['au_id'],
                v_s_id = sheet_id,
                v_date = datetime.now())

    # Save to database
    db_session.bulk_save_objects([sheet_record, view_record])
    db_session.commit()


def make_sheet_public(sheet_id):
    # Get Google ID
    record = sheet.query.filter_by(s_id=sheet_id).first()
    google_id = record.s_google_id

    # Update Google Drive permissions
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(http=httplib2.Http())
    service = build('drive', 'v3', http=http)
    permission_details = {
    'type': 'anyone',
    'role': 'reader',
    'allowFileDiscovery': False
    }
    response = service.permissions().create(
        fileId=google_id,
        body=permission_details,
        fields='id'
        ).execute()

    # Update Database
    record.s_shared = True
    db_session.commit()
