# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
from datetime import datetime
from flask import session

from apiclient.discovery import build
from sqlalchemy import update

import httplib2
from oauth2client import client

from app.lib.models import Base, sheet, view, db_session

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
                   "WHERE s_au_id = " + str(session['au_id']))

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
    service = build('drive', 'v3', http=http)
    response = service.files().get(fileId=g_id, fields='name, modifiedTime').execute()

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

def import_sheet_data(google_id):
    meta_data = get_sheet_meta(google_id)
    sheet_name = meta_data['name']
    last_modified = meta_data['modifiedTime']
    row_count = get_sheet_rows(google_id)

    # Insert new record
    record = sheet( s_au_id = session['au_id'],
                    s_ca_id = None,
                    s_sca_id = None,
                    s_google_id = google_id,
                    s_sheet_name = sheet_name,
                    s_row_count = row_count,
                    s_last_modified = last_modified,
                    s_shared = False,
                    s_date_shared = None,
                    s_hide_sharer = True)
    db_session.add(record)
    db_session.commit()
    current_sheet = sheet.query.filter_by(s_google_id = google_id).first()
    s_id = current_sheet.s_id

    # Update View Table
    current_view = view(v_au_id = session['au_id'],
                v_s_id = s_id,
                v_date = datetime.now())
    db_session.add(current_view)
    db_session.commit()

    return s_id

def save_sheet_info(sheet_id, google_id):
    # Get latest sheet meta data
    meta_data = get_sheet_meta(google_id)
    sheet_name = meta_data['name']
    last_modified = meta_data['modifiedTime']
    row_count = get_sheet_rows(google_id)

    record = sheet.query.filter_by(s_id=sheet_id).first()
    record.s_sheet_name = sheet_name
    record.s_row_count = row_count
    record.s_last_modified = last_modified
    db_session.commit()

    # Add new record to view table
    current_view = view(v_au_id = session['au_id'],
                v_s_id = sheet_id,
                v_date = datetime.now())
    db_session.add(current_view)
    db_session.commit()

def make_sheet_public(sheet_id):
    # Update Database
    record = sheet.query.filter_by(s_id=sheet_id).first()
    record.s_shared = True
    db_session.commit()
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
        fields='id',
        ).execute()
