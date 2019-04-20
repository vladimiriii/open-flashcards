# -*- coding: utf-8 -*-
from flask import session

# Google API
from googleapiclient.discovery import build
import google.oauth2.service_account


# Service Account Key and Scopes
SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]


def get_data():

    # Get Data
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES)

    # Create access object
    service = build('sheets', 'v4', credentials=credentials)

    response = query_API(service=service, sheet_id=session['google_id'])
    final_data = process_data(response)

    return final_data


def query_API(service, sheet_id):

    rangeName = 'A1:J'
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=rangeName).execute()
    values = result.get('values', [])

    return values


def process_data(response):

    results = {}
    results['headers'] = response[0]
    results['data'] = response[1:len(response)]

    return results
