# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
import json
from flask import session

# Google API
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Custom Libraries
from app.lib.models import Base, sheet, db_session
from app.lib.processLogin import credentials_to_dict

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO



###############################################
# Functions                                   #
###############################################

def initialize_reporting():

    try:
        # Get credentials from session
        credentials = Credentials(**session['credentials'])

        # Create access object
        service = build('sheets', 'v4', credentials=credentials)

        # Save credentials back in case the access token was refreshed
        session['credentials'] = credentials_to_dict(credentials)

        return service

    except:
        message = "{\"Error Type\": \"" + str(sys.exc_info()[0]) + "\", \"Error Value\": \"" + str(sys.exc_info()[1]) + "\", \"Error Traceback\": \"" + str(sys.exc_info()[2]) + "\"}"
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


def get_data():

    # Get Data
    service_object = initialize_reporting()
    response = query_API(service=service_object, sheet_id=session['google_id'])
    final_data = process_data(response)

    return final_data
