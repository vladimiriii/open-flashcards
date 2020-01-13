# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, session, redirect, url_for, request
import os
import sys

# Google API
import google.oauth2.credentials
import google.oauth2.service_account
import google_auth_oauthlib.flow

# Custom Libraries
import app.lib.cardData as cd
import app.lib.processLogin as pl
import app.lib.processSheets as ps

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'YES'

# Define the blueprint:
basic_page = Blueprint('basic_page', __name__)
internal_page = Blueprint('internal_page', __name__)
google_api = Blueprint('google_api', __name__)

# Service Account Key and Scopes
CLIENT_SECRETS_FILE = "app/static/data/private/client_secret.json"
SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"
SCOPES = [
    'openid email profile',
    # 'https://www.googleapis.com/auth/spreadsheets.readonly',
    # 'https://www.googleapis.com/auth/drive.readonly'
]


# BASIC PAGES
@basic_page.route('/', methods=['GET'])
def landing_page():
    try:
        if 'credentials' in session:
            return redirect(url_for('internal_page.dashboard_page'))
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


# GOOGLE API INTERACTIONS
@google_api.route('/process-login', methods=['GET'])
def process_login():
    try:
        # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

        flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',  # Refresh an access token without re-prompting the user for permission.
            include_granted_scopes='true'  # Enable incremental authorization
        )

        # Store the state so the callback can verify the auth server response.
        session['state'] = state

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

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
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


@basic_page.route('/flashcards/<sheet_id>')
def show_blog(sheet_id):
    try:
        if 'credentials' in session:
            permission_level = pl.check_user_role()
        else:
            permission_level = 'guest'

        return render_template('flashcards-template.html', sheet_id=sheet_id, permission_level=permission_level)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


# LOGGED IN PAGES
@internal_page.route('/dashboard', methods=['GET'])
def dashboard_page():
    try:
        if 'credentials' in session:
            permission_level = pl.check_user_role()
            return render_template('dashboard.html', value=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/admin')
def admin_page():
    try:
        if 'credentials' in session:
            permission_level = pl.check_user_role()

            if permission_level == 'super_user':
                return render_template('sheet-management.html')
            else:
                return redirect(url_for('internal_page.dashboard_page'))

        else:
            return redirect(url_for('basic_page.landing_page'))

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/logout', methods=['GET'])
def lo_page():
    try:
        session.clear()
        return redirect(url_for('basic_page.landing_page'))
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))

# Card Creation Options
@internal_page.route('/create-flashcards', methods=['GET'])
def create_flashcards_page():
    try:
        if 'credentials' in session:
            permission_level = pl.check_user_role()
            return render_template('create-flashcards.html', permission_level=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/get-sheet-lists', methods=['GET'])
def get_sheet_lists():
    try:
        public_list = ps.get_public_sheets()
        user_list = ps.get_user_sheets(session['au_id'])
        results = {"user_list": user_list, "public_list": public_list}
        return jsonify(results)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


# DATA ROUTES
@google_api.route('/register-sheet', methods=['POST'])
def register_sheet():
    try:
        google_id = request.data.decode('UTF-8')
        response = ps.import_new_sheet(google_id)
        return jsonify(response)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/register-sheet-view', methods=['POST'])
def save_page():
    try:
        # Saves Sheet ID to Session
        inputs = json.loads(request.data)
        session['sheet_id'] = inputs['sheetID']
        session['google_id'] = inputs['googleID']
        session.modified = True

        ps.update_sheet_metadata(session['sheet_id'], session['google_id'])
        ps.add_sheet_view(session['sheet_id'])

        return jsonify({"status": "Success"})
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/card-data', methods=['POST'])
def output_card_data():
    try:
        inputs = json.loads(request.data)
        sheet_id = inputs['sheetID']
        results = cd.get_data(sheet_id)
        return jsonify(results)
    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))
