# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
import json
from flask import session

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

from apiclient.discovery import build

import httplib2
from oauth2client import client

###############################################
# Functions                                   #
###############################################

def initialize_reporting():

    try:
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

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
    # Get Configuration Details
    SHEET_ID = session['sheet_id']

    # Get Data
    service_object = initialize_reporting()
    response = query_API(service=service_object, sheet_id=SHEET_ID)
    final_data = process_data(response)

    return final_data
