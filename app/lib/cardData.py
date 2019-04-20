# -*- coding: utf-8 -*-
# Google API
from googleapiclient.discovery import build
import google.oauth2.service_account
from googleapiclient.errors import HttpError

from app.lib.models import db_session  # view, app_user_rel_sheet
from app.lib.errorLookup import error_lookup


# Service Account Key and Scopes
SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]


def get_data(id):

    # Get Data
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES)

    # Create access object
    service = build('sheets', 'v4', credentials=credentials)

    # Access the data
    google_id = get_google_id(id)

    if google_id is not None:
        response = query_API(service=service, sheet_id=google_id)
        if 'error' not in response:
            final_data = process_data(response)
        else:
            final_data = response
    else:
        final_data = {'error': error_lookup['id_not_found']}

    return final_data


def get_google_id(id):

    # Query database
    query = (f"""
        SELECT s_google_id
        FROM sheet
        WHERE s_id = {id}
        LIMIT 1;
        """)

    try:
        query_data = db_session.execute(query).first()
    except:
        query_data = None

    if query_data is not None:
        google_id = query_data[0]
    else:
        google_id = None

    return google_id


def query_API(service, sheet_id):

    rangeName = 'A1:J'
    try:
        result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=rangeName).execute()
        values = result.get('values', [])
    except HttpError as err:
        if err.resp.status in error_lookup:
            values = {'error': error_lookup[err.resp.status]}
        else:
            values = {'error': error_lookup['other']}

    return values


def process_data(response):

    results = {}
    results['headers'] = response[0]
    results['data'] = response[1:len(response)]

    return results
