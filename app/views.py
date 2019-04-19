# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, session, redirect, url_for, request
import os
import sys
# import requests
# import argparse

# Google API
import google.oauth2.credentials
import google.oauth2.service_account


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
SERVICE_ACCOUNT_FILE = "app/static/data/private/service_account.json"
SCOPES = {
    "initial": [
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
}


# BASIC PAGES
@basic_page.route('/', methods=['GET'])
def la_page():
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

        credentials = google.oauth2.service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES['initial'])

        session['scope_status'] = 'initial'
        session['credentials'] = pl.credentials_to_dict(credentials)

        return redirect(url_for('internal_page.dashboard_page'))

    except:
        print(pl.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/get-sheet-lists', methods=['GET'])
def get_sheet_lists():
    try:
        # Get lists of available sheets
        # user_list = ps.get_user_sheets()
        public_list = ps.get_public_sheets()
        results = {"user_list": None, "public_list": public_list}
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

        # If scope present, update sheet meta
        scope_present = 'https://www.googleapis.com/auth/drive' in session['credentials']['scopes']
        if scope_present:
            ps.update_sheet_meta(session['sheet_id'], session['google_id'])

        return jsonify({"status": "Success"})
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
