# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, session, redirect, url_for, current_app, request
from datetime import date
import pandas as pd
import os
import sys
import httplib2
import requests
import argparse
from apiclient.discovery import build
from oauth2client import client

# Custom Libraries
import app.lib.cardData as cd
import app.lib.processLogin as pl
import app.lib.processSheets as ps

# Define the blueprint:
landing_page = Blueprint('landing_page', __name__)
privacy_policy = Blueprint('privacy_policy', __name__)
terms_conditions = Blueprint('terms_conditions', __name__)
process_login = Blueprint('process_login', __name__)
user_dashboard = Blueprint('user_dashboard', __name__)
get_sheet_lists = Blueprint('get_sheet_lists', __name__)
import_sheet = Blueprint('import_sheet', __name__)
save_sheet = Blueprint('save_sheet', __name__)
logout = Blueprint('logout', __name__)
cards_page = Blueprint('cards_page', __name__)
card_data = Blueprint('card_data', __name__)
error_page = Blueprint('error_page', __name__)

# Set scopes
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/userinfo.email']


@landing_page.route('/', methods=['GET'])
def la_page():
    try:
        if 'credentials' in session:
            credentials = client.OAuth2Credentials.from_json(session['credentials'])
            if not credentials.access_token_expired:
                return redirect(url_for('user_dashboard.dashboard_page'))
            else:
                return render_template('index.html')
        else:
            return render_template('index.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@privacy_policy.route('/privacy-policy', methods=['GET'])
def pp_page():
    try:
        return render_template('privacy_policy.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@terms_conditions.route('/terms-conditions', methods=['GET'])
def tc_page():
    try:
        return render_template('terms_conditions.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@process_login.route('/process-login', methods=['GET', 'POST'])
def oauth2callback():
    try:
        client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret_71572721139-4k4cch634h94b76f1qelmvuqpr6jv4da.apps.googleusercontent.com.json')
        if 'credentials' not in session:
            flow = client.flow_from_clientsecrets(
                client_secrets_path,
                scope=scopes,
                redirect_uri=url_for('process_login.oauth2callback', _external=True))

            if 'code' not in request.args:
                auth_uri = flow.step1_get_authorize_url()
                return redirect(auth_uri)
            else:
                auth_code = request.args.get('code')
                credentials = flow.step2_exchange(auth_code)
                session['credentials'] = credentials.to_json()

                return redirect(url_for('user_dashboard.dashboard_page'))

        credentials = client.OAuth2Credentials.from_json(session['credentials'])

        if credentials.access_token_expired:
            flow = client.flow_from_clientsecrets(
                client_secrets_path,
                scope=scopes,
                redirect_uri=url_for('process_login.oauth2callback', _external=True))

            if 'code' not in request.args:
                auth_uri = flow.step1_get_authorize_url()
                return redirect(auth_uri)
            else:
                auth_code = request.args.get('code')
                credentials = flow.step2_exchange(auth_code)
                session['credentials'] = credentials.to_json()
                return redirect(url_for('user_dashboard.dashboard_page'))
        else:
            return redirect(url_for('user_dashboard.dashboard_page'))
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@user_dashboard.route('/dashboard', methods=['GET'])
def dashboard_page():
    try:
        # If no credentials (i.e. user is logged out), kick user to landing page
        if 'credentials' not in session:
            return redirect(url_for('landing_page.la_page'))

        else:
            pl.process_login()
            credentials = client.OAuth2Credentials.from_json(session['credentials'])
            # If credentials have expired refresh them
            if credentials.access_token_expired:
                client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret_71572721139-4k4cch634h94b76f1qelmvuqpr6jv4da.apps.googleusercontent.com.json')
                flow = client.flow_from_clientsecrets(
                    client_secrets_path,
                    scope=scopes,
                    redirect_uri=url_for('process_login.oauth2callback', _external=True))

                if 'code' not in request.args:
                    auth_uri = flow.step1_get_authorize_url()
                    return redirect(auth_uri)
                else:
                    auth_code = request.args.get('code')
                    credentials = flow.step2_exchange(auth_code)
                    session['credentials'] = credentials.to_json()

            return render_template('dashboard.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))

@get_sheet_lists.route('/get-sheets', methods=['GET', 'POST'])
def get_lists():
    try:
        # Determine request type
        inputs = json.loads(request.data)
        request_type = inputs['requestType']

        # Return Account Map and Selected Sheet ID (if it exists)
        if request_type == 'initial view':
            sheet_list = ps.get_initial_view()
            results = {"sheets": sheet_list}
            return jsonify(results)

        # Saves Sheet ID to Session
        elif request_type == 'full list':
            sheet_list = ps.get_full_list()
            results = {"sheets": sheet_list}
            return jsonify(results)
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@import_sheet.route('/import-sheet', methods=['POST'])
def imp_sheet():
    try:
        inputs = json.loads(request.data)
        g_id = inputs['sheetID']
        s_id = ps.save_sheet_info(None, g_id)
        session['sheet_id'] = s_id
        session['google_id'] = g_id
        return jsonify({"status": "Success"})
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@save_sheet.route('/save-sheet', methods=['GET', 'POST'])
def save_page():
    try:
        # Saves Sheet ID to Session
        inputs = json.loads(request.data)
        session['sheet_id'] = inputs['sheetID']
        session['google_id'] = inputs['googleID']
        session.modified = True
        ps.save_sheet_info(session['sheet_id'], session['google_id'])
        return jsonify({"status": "Success"})
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@cards_page.route('/view-cards', methods=['GET'])
def vc_page():
    try:
        if 'credentials' not in session:
            return redirect(url_for('landing_page.la_page'))
        else:
            credentials = client.OAuth2Credentials.from_json(session['credentials'])

            # If credentials have expired refresh them
            if credentials.access_token_expired:
                client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret_71572721139-4k4cch634h94b76f1qelmvuqpr6jv4da.apps.googleusercontent.com.json')
                flow = client.flow_from_clientsecrets(
                    client_secrets_path,
                    scope=scopes,
                    redirect_uri=url_for('process_login.oauth2callback', _external=True))

                if 'code' not in request.args:
                    auth_uri = flow.step1_get_authorize_url()
                    return redirect(auth_uri)
                else:
                    auth_code = request.args.get('code')
                    credentials = flow.step2_exchange(auth_code)
                    session['credentials'] = credentials.to_json()

            return render_template('cards.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))


@card_data.route('/card-data', methods=['GET'])
def output_card_data():
    try:
        results = cd.get_data()
        return jsonify(results)
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return message


@error_page.route('/error', methods=['GET'])
def er_page():
    return render_template('error.html')


@logout.route('/logout', methods=['GET'])
def lo_page():
    try:
        session.clear()
        return redirect(url_for('landing_page.la_page'))
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('error_page.er_page'))
