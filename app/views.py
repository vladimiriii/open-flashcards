# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, session, redirect, url_for, request  # , current_app
# from datetime import date
# import pandas as pd
import os
import sys
# import requests
# import argparse

# Google API
import google.oauth2.credentials
import google_auth_oauthlib.flow
# import googleapiclient.discovery

# Custom Libraries
import app.lib.cardData as cd
import app.lib.processLogin as pl
import app.lib.processSheets as ps

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'YES'

# Define the blueprint:
basic_page = Blueprint('basic_page', __name__)
internal_page = Blueprint('internal_page', __name__)
google_api = Blueprint('google_api', __name__)

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "app/static/data/private/client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = {
    "initial": [
        'https://www.googleapis.com/auth/plus.me',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ],
    "add": [
        'https://www.googleapis.com/auth/drive.readonly'
    ],
    "share": [
        'https://www.googleapis.com/auth/drive'
    ]
}


# BASIC PAGES
@basic_page.route('/', methods=['GET'])
def la_page():
    try:
        if 'credentials' in session:
            credentials = google.oauth2.credentials.Credentials(**session['credentials'])

            if not credentials.access_token_expired:
                return redirect(url_for('internal_page.dashboard_page'))
            else:
                return render_template('index.html')
        else:
            return render_template('index.html')
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/privacy-policy', methods=['GET'])
def pp_page():
    try:
        return render_template('privacy_policy.html')
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/terms-conditions', methods=['GET'])
def tc_page():
    try:
        return render_template('terms_conditions.html')
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/error', methods=['GET'])
def er_page():
    return render_template('error.html')


# LOGGED IN PAGES
@internal_page.route('/dashboard', methods=['GET'])
def dashboard_page():
    try:
        # If no credentials (i.e. user is logged out), kick user to landing page
        if 'credentials' not in session:
            return redirect(url_for('basic_page.la_page'))
        else:
            return render_template('dashboard.html')
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/view-cards', methods=['GET'])
def vc_page():
    try:
        if 'credentials' not in session:
            return redirect(url_for('basic_page.la_page'))
        else:
            return render_template('cards.html')
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/logout', methods=['GET'])
def lo_page():
    try:
        session.clear()
        return redirect(url_for('basic_page.la_page'))
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


# GOOGLE API INTERACTIONS
@google_api.route('/process-login', methods=['GET'])
def process_login():
    try:
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES['initial'])

        flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',  # Refresh an access token without re-prompting the user for permission.
            include_granted_scopes='true'  # Enable incremental authorization
        )

        # Store the state so the callback can verify the auth server response.
        session['state'] = state
        session['scope_status'] = 'initial'

        return redirect(authorization_url)

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/add-drive-read-scope', methods=['GET'])
def get_drive_read_scope():
    try:
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES['add'])

        flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',  # Refresh an access token without re-prompting the user for permission.
            include_granted_scopes='true'  # Enable incremental authorization
        )

        # Store the state so the callback can verify the auth server response.
        session['state'] = state
        session['scope_status'] = 'add'

        return redirect(authorization_url)

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/add-drive-share-scope', methods=['GET'])
def get_drive_share_scope():
    try:
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES['share'])

        flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',  # Refresh an access token without re-prompting the user for permission.
            include_granted_scopes='true'  # Enable incremental authorization
        )

        # Store the state so the callback can verify the auth server response.
        session['state'] = state
        session['scope_status'] = 'share'

        return redirect(authorization_url)

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/oauth2callback')
def oauth2callback():
    try:
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = session['state']
        status = session['scope_status']

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES[status],
            state=state
        )

        flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        # Store credentials in the session.
        credentials = flow.credentials
        session['credentials'] = pl.credentials_to_dict(credentials)
        pl.process_login()

        return redirect(url_for('internal_page.dashboard_page'))
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/get-sheet-lists', methods=['GET'])
def get_sheet_lists():
    try:
        # Get lists of available sheets
        user_list = ps.get_user_sheets()
        public_list = ps.get_public_sheets()
        results = {"user_list": user_list, "public_list": public_list}
        return jsonify(results)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/view-sheet', methods=['POST'])
def save_page():
    try:
        # Saves Sheet ID to Session
        inputs = json.loads(request.data)
        session['sheet_id'] = inputs['sheetID']
        session['google_id'] = inputs['googleID']
        session.modified = True

        # Add record of views
        ps.add_view_record(session['sheet_id'], session['google_id'])

        # If scope present, update sheet meta
        scope_present = 'https://www.googleapis.com/auth/drive' in session['credentials']['scopes']
        if scope_present:
            ps.update_sheet_meta(session['sheet_id'], session['google_id'])

        return jsonify({"status": "Success"})
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/check-drive-scopes', methods=['GET'])
def check_scopes():
    try:
        read_scope_present = 'https://www.googleapis.com/auth/drive.readonly' in session['credentials']['scopes']
        modify_scope_present = 'https://www.googleapis.com/auth/drive' in session['credentials']['scopes']
        return jsonify({
            "read_scope_present": str(read_scope_present),
            "modify_scope_present": str(modify_scope_present)
            })

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/get-import-options', methods=['GET'])
def get_import_list():
    try:
        # Get a list of sheets from user's drive that can be imported
        sheet_list = ps.get_full_list()
        results = {"sheets": sheet_list}
        return jsonify(results)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/import-sheet', methods=['POST'])
def imp_sheet():
    try:
        inputs = json.loads(request.data)
        g_id = inputs['sheetID']
        s_id = ps.import_sheet_data(g_id)
        session['sheet_id'] = s_id
        session['google_id'] = g_id
        session.modified = True
        return jsonify({"status": "Success"})
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/make-sheet-public', methods=['POST'])
def open_sheet_permissions():
    try:
        if request.data is not None:
            inputs = json.loads(request.data)
            session.modified = True

            # Open sheet permissions
            ps.make_sheet_public(inputs['sheetID'])

        return jsonify({"status": "sheet shared"})
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/card-data', methods=['GET'])
def output_card_data():
    try:
        results = cd.get_data()
        return jsonify(results)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))

# @drive_access.route('/drive-access', methods=['GET'])
# def get_drive_access():
#     try:
#         scopes.append('https://www.googleapis.com/auth/drive')
#         client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret.json')
#         flow = client.flow_from_clientsecrets(
#             client_secrets_path,
#             scope = scopes,
#             redirect_uri = url_for('drive_access.get_drive_access', _external = True))
#
#         if 'code' not in request.args:
#             auth_uri = flow.step1_get_authorize_url()
#             return redirect(auth_uri)
#         else:
#             auth_code = request.args.get('code')
#             credentials = flow.step2_exchange(auth_code)
#             session['credentials'] = credentials.to_json()
#
#         # Update session to reflect new scope
#         session['drive_access'] = True
#         session.modified = True
#         dataJSON = {"sheetID": session['shared_sheet_id']}
#         response = requests.post('http://localhost:8888/open-sheet', json=dataJSON)
#         print(response)
#         return jsonify({"status": "access granted"})
#         # return redirect(url_for('open_sheet.open_sheet_permissions', messages=dataJSON, code=307))
#     except:
#         print(pl.generate_error_message(sys.exc_info()))
#         return redirect(url_for('basic_page.er_page'))
