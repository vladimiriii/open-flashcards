# -*- coding: utf-8 -*-
import pandas as pd
import os, shutil
from datetime import datetime
from flask import session

from apiclient.discovery import build

import httplib2
from oauth2client import client

from app.lib.models import Base, sheet, view, db_session

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

def save_sheet_info(sheet_id):
    # Query DB
    current_sheet = sheet.query.filter_by(s_google_id = sheet_id).first()

    if current_sheet is None:
        record = sheet( s_au_id = session['au_id'],
                        s_ca_id = None,
                        s_sca_id = None,
                        s_google_id = sheet_id,
                        s_row_count = None,
                        s_last_modified = None,
                        s_shared = False,
                        s_date_shared = None,
                        s_hide_sharer = True)
        db_session.add(record)
        db_session.commit()
        current_sheet = sheet.query.filter_by(s_google_id = sheet_id).first()

    # Update View Table
    current_view = view(v_au_id = session['au_id'],
                v_s_id = current_sheet.s_id,
                v_date = datetime.now())
    db_session.add(current_view)
    db_session.commit()
