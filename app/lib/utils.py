from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials as service_account_credentials
from google.oauth2.credentials import Credentials as user_credentials

from flask import session
from app.lib.database.models import app_user, app_user_role, db_session

SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"


def get_drive_client_credentials():
    credentials = user_credentials(**session['credentials'])
    service = build('drive', 'v3', credentials=credentials)
    session['credentials'] = credentials_to_dict(credentials)

    return service


def get_sheets_client_credentials():
    credentials = user_credentials(**session['credentials'])
    service = build('sheets', 'v4', credentials=credentials)
    session['credentials'] = credentials_to_dict(credentials)

    return service


def get_drive_service_account_credentials():
    credentials = service_account_credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive.readonly'])

    service = build('drive', 'v3', credentials=credentials)

    return service


def get_sheets_service_account_credentials():
    credentials = service_account_credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

    service = build('sheets', 'v4', credentials=credentials)

    return service


def get_drive_credentials():
    if 'credentials' in session:
        service = get_drive_client_credentials()
    else:
        service = get_drive_service_account_credentials()

    return service


def get_sheets_credentials():
    if 'credentials' in session:
        service = get_sheets_client_credentials()
    else:
        service = get_sheets_service_account_credentials()

    return service


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}


def check_user_role():
    user_role = (db_session.query(app_user, app_user_role)
                           .filter(app_user.au_email == session['email'])
                           .filter(app_user.au_aur_id == app_user_role.aur_id)
                           .first()).app_user_role.aur_role_name

    return user_role


def generate_error_message(sys_info):
    message = "ERROR FOUND\nError Type: \"" + str(sys_info[0]) + "\"\nError Value: \"" + str(
        sys_info[1]) + "\"\nError Traceback: \"" + str(sys_info[2]) + "\""
    return message
