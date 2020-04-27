from googleapiclient.errors import HttpError

from app.lib.database.models import db_session, sheet, app_user_rel_sheet, sheet_status
from app.lib import utils


def get_public_sheets():
    query = ("""
        SELECT s_id,
            s_google_id,
            FALSE as aurs_is_owner,
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
            aurs_is_owner,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0) AS views,
            ss_status_name,
            s_last_modified
        FROM sheet AS s
        INNER JOIN (
            SELECT aurs_s_id
                , aurs_is_owner
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
    query = ("""
        SELECT s_id,
            s_google_id,
            FALSE AS aurs_is_owner,
            s_sheet_name,
            s_row_count,
            COALESCE(views, 0) AS views,
            ss_status_name,
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
        WHERE ss_status_name = 'Review Requested';
        """)

    data = db_session.execute(query)

    return data


def check_user_has_access(sheet_id, user_id):

    result = app_user_rel_sheet.query.filter_by(aurs_s_id=sheet_id).filter_by(aurs_au_id=user_id).first()

    if result is not None:
        return True
    else:
        return False


def check_sheet_is_public(sheet_id):

    status = (db_session.query(sheet_status.ss_status_name)
                        .filter(sheet.s_ss_id == sheet_status.ss_id)
                        .filter(sheet.s_id == sheet_id)
                        .scalar())
    if status == 'Public':
        return True
    else:
        return False


def get_sheet_metadata(google_id):
    service = utils.get_drive_credentials()

    fields = "name, createdTime, modifiedTime, owners, ownedByMe"
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
    metadata['is_owner'] = raw_metadata['ownedByMe']

    return metadata


def get_sheet_row_count(google_id):
    service = utils.get_sheets_credentials()

    # Get sheet row count
    rangeName = 'A1:Z'
    result = service.spreadsheets().values().get(spreadsheetId=google_id, range=rangeName).execute()

    return len(result.get('values', [])) - 1


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
