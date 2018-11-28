# -*- coding: utf-8 -*-
import os, shutil
import json
from datetime import datetime
from flask import session

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from app.lib.models import Base, app_user, db_session


def process_login():

    # Get credentials from session
    credentials = Credentials(**session['credentials'])

    # Create access object
    service = build('plus', 'v1', credentials=credentials)

    # Get profile info
    profile_info = service.people().get(userId='me').execute()

    print(profile_info)

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

    # Save credentials back in case the access token was refreshed
    session['credentials'] = credentials_to_dict(credentials)


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def generate_error_message(sys_info):
    message = "ERROR FOUND\nError Type: \"" + str(sys_info[0]) + "\"\nError Value: \"" + str(
        sys_info[1]) + "\"\nError Traceback: \"" + str(sys_info[2]) + "\""
    return message
