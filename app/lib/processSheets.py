# -*- coding: utf-8 -*-
from datetime import datetime
from flask import session
import pandas as pd

# Google API
from googleapiclient.errors import HttpError

# Custom Libraries
from app.lib.database.models import sheet, db_session, view, app_user_rel_sheet, sheet_status, sheet_action, sheet_action_type
from app.lib import utils
from app.lib import reference as ref


def get_public_sheets():
    query = ("""
        SELECT s_id,
            s_google_id,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0) AS views,
            s_last_modified
        FROM sheet AS s
        INNER JOIN sheet_status
        ON s_ss_id = ss_id
        LEFT JOIN (
            SELECT v_s_id,
                COUNT(v_id) AS views
            FROM public.view
            GROUP BY v_s_id
            ORDER BY views DESC
            ) AS vs
        ON s.s_id = vs.v_s_id
        WHERE ss_status_name = 'Public';
        """)

    data = db_session.execute(query)

    return data


def get_user_sheets(user_id):
    query = (f"""
        SELECT s_id,
            s_google_id,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0) AS views,
            ss_status_name,
            s_last_modified
        FROM sheet AS s
        INNER JOIN (
            SELECT aurs_s_id
            FROM app_user_rel_sheet
            WHERE aurs_au_id = {user_id}
            AND NOT aurs_deleted
        ) AS aurs
        ON aurs_s_id = s_id
        INNER JOIN sheet_status
        ON s_ss_id = ss_id
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

    return data


def get_request_sheets():
    query = (f"""
        SELECT s_id,
            s_google_id,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0) AS views,
            ss_status_name,
            s_last_modified
        FROM sheet AS s
        INNER JOIN sheet_status
        ON s_ss_id = ss_id
        INNER JOIN (
            SELECT v_s_id,
                COUNT(v_id) AS views
            FROM public.view
            GROUP BY v_s_id
            ORDER BY views DESC
            ) AS vs
        ON s.s_id = vs.v_s_id
        WHERE ss_status_name = 'Review Requested';
        """)

    data = db_session.execute(query)

    return data


def process_sheet_data(data):
    df = pd.DataFrame(data)
    if len(df) > 0:
        df.columns = [ref.column_lookup[col] for col in data.keys()]
        data_dict = df.to_dict(orient='split')
    else:
        data_dict = None
    return data_dict


def get_sheet_metadata(google_id):
    service = utils.get_drive_credentials()

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
    status_id = db_session.query(sheet_status.ss_id).filter_by(ss_status_name='Private').first()
    sheet_record = sheet(s_ss_id=status_id,
                         s_google_id=metadata['google_id'],
                         s_sheet_name=metadata['sheet_name'],
                         s_owner_name=metadata['owner_name'],
                         s_owner_email=metadata['owner_email'],
                         s_row_count=metadata['row_count'],
                         s_sheet_created=metadata['created_date'],
                         s_sheet_last_modifed=metadata['last_modified'],
                         s_created=datetime.utcnow(),
                         s_last_modified=datetime.utcnow(),
                         )
    db_session.add(sheet_record)
    db_session.commit()

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
    sheet_record.s_sheet_last_modifed = metadata['last_modified']
    sheet_record.s_last_modifed = datetime.utcnow()

    # Commit changes to the database
    db_session.commit()


def add_sheet_view(sheet_id):
    if 'au_id' in session:
        view_record = view(v_au_id=session['au_id'],
                           v_s_id=sheet_id,
                           v_timestamp=datetime.now())
    else:

        view_record = view(v_au_id=1,
                           v_s_id=sheet_id,
                           v_timestamp=datetime.now())

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

    return response


def get_sheet_row_count(google_id):
    service = utils.get_sheets_credentials()

    # Get sheet row count
    rangeName = 'A1:Z'
    result = service.spreadsheets().values().get(spreadsheetId=google_id, range=rangeName).execute()

    return len(result.get('values', []))


def check_sheet_availability(google_id):
    response = {}
    try:
        drive_service = utils.get_drive_service_account_credentials()
        sheet_service = utils.get_sheets_service_account_credentials()
        drive_service.files().get(fileId=google_id, fields='name').execute()
        sheet_service.spreadsheets().values().get(spreadsheetId=google_id, range='A1:J').execute()
        response['status'] = "sheet_accessible"
    except HttpError as e:
        if e.resp.status == 404:
            response['status'] = 'sheet_not_accessible'
        else:
            response['status'] = 'unknown_error'

    return response


def update_sheet_status(google_id, event):

    if event == 'Request Public':
        permission_level = utils.check_user_role()
        if permission_level == 'Super User':
            event = "Make Public"

    sheet_id = db_session.query(sheet.s_id).filter_by(s_google_id=google_id).first()
    action_type_id = db_session.query(sheet_action_type.sat_id).filter_by(sat_type_name=event).first()

    new_event = sheet_action(
        sa_sat_id=action_type_id,
        sa_au_id=session['au_id'],
        sa_s_id=sheet_id,
        sa_timestamp=datetime.utcnow()
    )
    db_session.add(new_event)
    db_session.commit()

    new_status = (db_session.query(sheet_status.ss_status_name)
                            .filter(sheet.s_ss_id == sheet_status.ss_id)
                            .filter(sheet.s_google_id == google_id)
                            .first())

    return new_status
