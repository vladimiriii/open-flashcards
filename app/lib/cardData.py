# -*- coding: utf-8 -*-
from flask import session

# Google API
from googleapiclient.discovery import build
import google.oauth2.service_account

# Custom Libraries
from app.lib.processLogin import credentials_to_dict

import sys

# Service Account Key and Scopes
SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"
SCOPES = {
    "initial": [
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
}


def get_data():

    # Get Data
    service_object = initialize_reporting()
    response = query_API(service=service_object, sheet_id=session['google_id'])
    final_data = process_data(response)

    return final_data


def initialize_reporting():

    try:

        credentials = google.oauth2.service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES['initial'])

        # Create access object
        service = build('sheets', 'v4', credentials=credentials)

        # Save credentials back in case the access token was refreshed
        session['credentials'] = credentials_to_dict(credentials)

        return service

    except:
        message = "{\"Error Type\": \"" + str(sys.exc_info()[0]) + "\", \"Error Value\": \""
        message += str(sys.exc_info()[1]) + "\", \"Error Traceback\": \"" + str(sys.exc_info()[2]) + "\"}"
        print(message)


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
