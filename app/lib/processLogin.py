# -*- coding: utf-8 -*-
import os, shutil
import json
from datetime import datetime
from flask import session

from apiclient.discovery import build
import httplib2
from oauth2client import client

from app.lib.models import Base, app_user, db_session

# def check_token_valid(scopes, client_secrets_path):
#     # If no credentials (i.e. user is logged out), kick user to landing page
#     if 'credentials' not in session:
#         return redirect(url_for('basic_page.la_page'))
#
#     else:
#         credentials = client.OAuth2Credentials.from_json(session['credentials'])
#         # If credentials have expired refresh them
#         if credentials.access_token_expired:
#             client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret.json')
#             flow = client.flow_from_clientsecrets(
#                 client_secrets_path,
#                 scope=scopes,
#                 redirect_uri=url_for('process_login.oauth2callback', _external=True))
#
#             if 'code' not in request.args:
#                 auth_uri = flow.step1_get_authorize_url()
#                 return redirect(auth_uri)
#             else:
#                 auth_code = request.args.get('code')
#                 credentials = flow.step2_exchange(auth_code)
#                 session['credentials'] = credentials.to_json()
#
#         return render_template('dashboard.html')

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

def generate_error_message(sys_info):
    message = "ERROR FOUND\nError Type: \"" + str(sys_info[0]) + "\"\nError Value: \"" + str(
        sys_info[1]) + "\"\nError Traceback: \"" + str(sys_info[2]) + "\""
    return message
