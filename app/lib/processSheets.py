# -*- coding: utf-8 -*-
from flask import session
# from sqlalchemy import update

# Google API
from googleapiclient.discovery import build

# Custom Libraries
from app.lib.models import sheet, db_session  # view, app_user_rel_sheet
from app.lib.processLogin import credentials_to_dict


def get_public_sheets():

    # Query database
    public_query = (f"""
        SELECT s_id,
            s_google_id,
            s_sheet_name,
            s_row_count,
            views,
            s_last_modified
        FROM sheet AS s
        INNER JOIN (
            SELECT v_s_id,
                COUNT(v_id) AS views
            FROM public.view
            GROUP BY v_s_id
            ORDER BY views DESC
            ) AS vs
        ON s.s_id = vs.v_s_id
        WHERE s_shared = TRUE;
        """)

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
            'modified': row[5]})

    return file_list


def get_sheet_meta(credentials, g_id):

    # Create access object
    service = build('drive', 'v3', credentials=credentials)

    # Get a list of all Sheets in the account for the current user.
    response = service.files().get(fileId=g_id, fields='name,modifiedTime,ownedByMe').execute()

    meta_data = {}
    for key in response:
        meta_data[key] = response[key]

    # Save credentials back in case the access token was refreshed
    session['credentials'] = credentials_to_dict(credentials)

    return meta_data


def get_sheet_rows(credentials, g_id):

    # Create access object
    service = build('sheets', 'v4', credentials=credentials)

    # Get sheet row count
    rangeName = 'A1:Z'
    result = service.spreadsheets().values().get(spreadsheetId=g_id, range=rangeName).execute()

    return len(result.get('values', []))


def update_sheet_meta(credentials, sheet_id, google_id):

    # Get latest sheet meta data
    meta_data = get_sheet_meta(credentials, google_id)
    sheet_name = meta_data['name']
    last_modified = meta_data['modifiedTime']
    row_count = get_sheet_rows(credentials, google_id)
    # owner_status = meta_data['ownedByMe']

    # Update sheet record with latest metadata
    sheet_record = sheet.query.filter_by(s_id=sheet_id).first()
    sheet_record.s_sheet_name = sheet_name
    sheet_record.s_row_count = row_count
    sheet_record.s_last_modified = last_modified

    # Commit changes to the database
    db_session.commit()
