# -*- coding: utf-8 -*-
from flask import session, url_for, request

# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Custom Libraries
from app.lib import utils

# Service Account Key and Scopes
CLIENT_SECRETS_FILE = utils.get_config_field('Google', 'CLIENT_SECRETS_FILE')
SERVICE_ACCOUNT_FILE = utils.get_config_field('Google', 'SERVICE_ACCOUNT_FILE')
SCOPES = [
    'openid email profile',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]


def process_login():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('google_api.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Refresh an access token without re-prompting the user for permission.
        include_granted_scopes='true'  # Enable incremental authorization
    )

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return authorization_url


def handle_callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = Flow.from_client_secrets_file(
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
    session['credentials'] = utils.credentials_to_dict(credentials)


def get_profile_info():
    credentials = Credentials(**session['credentials'])
    service = build('oauth2', 'v2', credentials=credentials)
    profile_info = service.userinfo().get().execute()
    session['credentials'] = utils.credentials_to_dict(credentials)

    return profile_info
