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
    email = profile_info['emails'][0].get('value')
    first_name = profile_info['name'].get('givenName')
    last_name = profile_info['name'].get('familyName')
    gender = profile_info.get('gender')
    profile_url = profile_info.get('url')

    # Query DB
    current_user = app_user.query.filter_by(au_email=email).first()

    if current_user is None:
        current_user = app_user(
            au_aur_id = 2,
            au_email = email,
            au_first_name = first_name,
            au_last_name = last_name,
            au_gender = gender,
            au_profile_url = profile_url,
            au_first_sign_in = datetime.now(),
            au_last_sign_in = datetime.now(),
            au_is_deleted = False
        )
        db_session.add(current_user)
        db_session.flush()
        db_session.commit()
        s_id = current_user.au_id
        print("Current user ID: %d" % s_id)
    else:
        current_user.au_last_sign_in = datetime.now()
        db_session.commit()

    # Save User ID to Session
    session['au_id'] = current_user.au_id
    session['email'] = email
