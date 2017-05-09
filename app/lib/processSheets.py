# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
import json
from flask import session

from apiclient.discovery import build

import httplib2
from oauth2client import client

# from app.lib.models import Base, sheet

###############################################
# Functions                                   #
###############################################

def get_sheet_list():
    # Get a list of all Sheets in the account for the current user.
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(http=httplib2.Http())
    # discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v3')
    service = build('drive', 'v3', http=http)
    response = service.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name, modifiedTime)').execute()

    file_list = []
    for file in response.get('files', []):
        # Process change
        file_list.append({
            'name': file.get('name'),
            'id': file.get('id'),
            'modified': file.get('modifiedTime')
            })

    return file_list

# def save_sheet_info():
