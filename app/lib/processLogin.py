# -*- coding: utf-8 -*-
import os, shutil
import json
from datetime import datetime
from flask import session

from apiclient.discovery import build
import httplib2
from oauth2client import client

from app.lib.models import Base, app_user, db_session

def process_login():

    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    http = credentials.authorize(http=httplib2.Http())
    service = build('plus', 'v1', http=http)
    profile_info = service.people().get(userId='me').execute()

    # Parse Information
    email = profile_info['emails'][0]['value']
    first_name = profile_info['name']['givenName']
    last_name = profile_info['name']['familyName']
    gender = profile_info['gender']
    profile_url = profile_info['url']

    # Query DB
    current_user = app_user.query.filter_by(au_email=email).first()

    if current_user is None:
        record = app_user(2,
                    email,
                    first_name,
                    last_name,
                    gender,
                    profile_url,
                    datetime.now(),
                    datetime.now(),
                    False)
        db_session.add(record)
        db_session.commit()
    else:
        current_user.au_last_sign_in = datetime.now()
        db_session.commit()
