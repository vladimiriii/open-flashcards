# -*- coding: utf-8 -*-
from datetime import datetime
from flask import session

# Google API
from googleapiclient.discovery import build
import google.oauth2.service_account
from googleapiclient.errors import HttpError

# Custom Libraries
from app.lib.models import sheet, db_session, view, app_user_rel_sheet

# Service Account Key and Scopes
SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]


def get_public_sheets():
    query = ("""
        SELECT s_id,
            s_google_id,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0),
            s_last_modified_date
        FROM sheet AS s
        LEFT JOIN (
            SELECT v_s_id,
                COUNT(v_id) AS views
            FROM public.view
            GROUP BY v_s_id
            ORDER BY views DESC
            ) AS vs
        ON s.s_id = vs.v_s_id
        WHERE s_is_public;
        """)

    data = db_session.execute(query)

    # Process Results
    file_list = []
    for row in data:
        file_list.append({
            'id': row[0],
            'google_id': row[1],
            'sheet_name': row[2],
            'row_count': row[3],
            'views': row[4],
            'modified': row[5]})

    return file_list


def get_user_sheets(user_id):
    query = (f"""
        SELECT s_id,
            s_google_id,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0),
            s_last_modified_date
        FROM sheet AS s
        INNER JOIN (
            SELECT aurs_s_id
            FROM public.app_user_rel_sheet
            WHERE aurs_au_id = {user_id}
            AND NOT aurs_deleted
        ) AS aurs
        ON aurs_s_id = s_id
        LEFT JOIN (
            SELECT v_s_id,
                COUNT(v_id) AS views
            FROM public.view
            GROUP BY v_s_id
            ORDER BY views DESC
            ) AS vs
        ON s.s_id = vs.v_s_id;
        """)

    data = db_session.execute(query)

    # Process Results
    file_list = []
    for row in data:
        file_list.append({
            'id': row[0],
            'google_id': row[1],
            'sheet_name': row[2],
            'row_count': row[3],
            'views': row[4],
            'modified': row[5]})

    return file_list


def get_sheet_metadata(google_id):
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    fields = "name, createdTime, modifiedTime, owners"
    raw_metadata = service.files().get(fileId=google_id, fields=fields).execute()

    # Create clean metadata object
    metadata = {}
    metadata['sheet_name'] = raw_metadata['name']
    metadata['google_id'] = google_id
    metadata['created_date'] = raw_metadata['createdTime']
    metadata['last_modified'] = raw_metadata['modifiedTime']
    metadata['owner_email'] = raw_metadata['owners'][0]['emailAddress']
    metadata['owner_name'] = raw_metadata['owners'][0]['displayName']
    metadata['row_count'] = get_sheet_row_count(google_id)
    metadata['is_owner'] = metadata['owner_email'] == session['email'] if 'email' in session else False

    return metadata


def add_new_sheet_entry(metadata):
    sheet_record = sheet(s_ca_id=None,
                         s_sca_id=None,
                         s_google_id=metadata['google_id'],
                         s_sheet_name=metadata['sheet_name'],
                         s_owner_name=metadata['owner_name'],
                         s_owner_email=metadata['owner_email'],
                         s_row_count=metadata['row_count'],
                         s_imported_date=datetime.utcnow(),
                         s_created_date=metadata['created_date'],
                         s_last_modified_date=metadata['last_modified'],
                         s_is_public=True,
                         s_made_public_date=datetime.utcnow()
                         )
    db_session.add(sheet_record)
    db_session.flush()

    return sheet_record.s_id


def add_new_user_rel_sheet_entry(sheet_id, is_owner):
    rel_record = app_user_rel_sheet(aurs_au_id=session['au_id'],
                                    aurs_s_id=sheet_id,
                                    aurs_first_view=datetime.now(),
                                    aurs_is_owner=is_owner,
                                    aurs_deleted=False)

    db_session.add(rel_record)
    db_session.commit()

    return rel_record.aurs_id


def update_sheet_metadata(sheet_id):
    google_id = db_session.query(sheet.s_google_id).filter_by(s_id=sheet_id).scalar()

    metadata = get_sheet_metadata(google_id)

    # Update sheet record with latest metadata
    sheet_record = sheet.query.filter_by(s_id=sheet_id).first()
    sheet_record.s_sheet_name = metadata['sheet_name']
    sheet_record.s_row_count = metadata['row_count']
    sheet_record.s_last_modified_date = metadata['last_modified']

    # Commit changes to the database
    db_session.commit()


def add_sheet_view(sheet_id):
    if 'au_id' in session:
        view_record = view(v_au_id=session['au_id'],
                           v_s_id=sheet_id,
                           v_date=datetime.now())
    else:

        view_record = view(v_au_id=1,
                           v_s_id=sheet_id,
                           v_date=datetime.now())

    # Save to Database
    db_session.add(view_record)
    db_session.commit()

    return view_record.v_id


def import_new_sheet(google_id):
    response = {}
    current_sheet = sheet.query.filter_by(s_google_id=google_id).first()

    try:
        metadata = get_sheet_metadata(google_id)

        if current_sheet is None:
            sheet_id = add_new_sheet_entry(metadata)
            add_new_user_rel_sheet_entry(sheet_id, metadata['is_owner'])
            response['status'] = 'sheet_imported'
        else:
            sheet_id = current_sheet.s_id
            update_sheet_metadata(sheet_id, google_id)

            # Check if this user already has relationship to this sheet
            sheet_rel_user = app_user_rel_sheet.query.filter_by(aurs_s_id=sheet_id, aurs_au_id=session['au_id']).first()
            if sheet_rel_user is None:
                add_new_user_rel_sheet_entry(sheet_id, metadata['is_owner'])
                response['status'] = 'sheet_imported'
            else:
                response['status'] = 'sheet_already_imported'

        response['sheetId'] = str(sheet_id)

    except HttpError as e:
        if e.resp.status == 404:
            response['status'] = 'sheet_not_exist'
        elif e.resp.status == 400:
            response['status'] = 'invalid_url'
        else:
            response['status'] = 'unknown_error'
    except Exception as e:
        response['status'] = 'unknown_error'

    return response


def get_sheet_row_count(google_id):
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    # Get sheet row count
    rangeName = 'A1:Z'
    result = service.spreadsheets().values().get(spreadsheetId=google_id, range=rangeName).execute()

    return len(result.get('values', []))


def check_sheet_availability(google_id):
    response = {}
    try:
        get_sheet_metadata(google_id)
        response['status'] = "sheet_accessible"
    except HttpError as e:
        if e.resp.status == 404:
            response['status'] = 'sheet_not_accessible'
        else:
            response['status'] = 'unknown_error'
    except Exception:
        response['status'] = 'unknown_error'

    return response
