# -*- coding: utf-8 -*-
from datetime import datetime
from flask import session

# Google API
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Custom Libraries
from app.lib.models import app_user, app_user_role, db_session


def process_login():

    # Get credentials from session
    credentials = Credentials(**session['credentials'])

    # Create access object
    service = build('oauth2', 'v2', credentials=credentials)

    # Get profile info
    profile_info = service.userinfo().get().execute()

    # Parse Information
    email = profile_info['email']
    first_name = profile_info['given_name']
    last_name = profile_info['family_name']

    # Lookup user
    current_user = app_user.query.filter_by(au_email=email).first()

    if current_user is None:
        current_user = app_user(
            au_aur_id=2,
            au_email=email,
            au_first_name=first_name,
            au_last_name=last_name,
            au_gender=None,
            au_profile_url=None,
            au_first_sign_in=datetime.now(),
            au_last_sign_in=datetime.now(),
            au_is_deleted=False
        )
        db_session.add(current_user)
        db_session.flush()
        db_session.commit()

    else:
        current_user.au_last_sign_in = datetime.now()
        db_session.commit()

    # Save credentials back in case the access token was refreshed
    session['credentials'] = credentials_to_dict(credentials)


def check_user_role():

    # Get credentials from session
    credentials = Credentials(**session['credentials'])

    # Create access object
    service = build('oauth2', 'v2', credentials=credentials)

    # Get profile info
    profile_info = service.userinfo().get().execute()

    # Check DB for role
    user_role = (db_session.query(app_user, app_user_role)
                           .filter(app_user.au_email == profile_info['email'])
                           .filter(app_user.au_aur_id == app_user_role.aur_id)
                           .first()).app_user_role.aur_role_name

    return user_role


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes}


def generate_error_message(sys_info):
    message = "ERROR FOUND\nError Type: \"" + str(sys_info[0]) + "\"\nError Value: \"" + str(
        sys_info[1]) + "\"\nError Traceback: \"" + str(sys_info[2]) + "\""
    return message
