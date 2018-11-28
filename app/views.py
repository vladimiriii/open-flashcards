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
basic_page = Blueprint('basic_page', __name__)
internal_page = Blueprint('internal_page', __name__)
google_api = Blueprint('google_api', __name__)

# Set scopes
scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/drive']


# BASIC PAGES
@basic_page.route('/', methods=['GET'])
def la_page():
    try:
        if 'credentials' in session:
            credentials = client.OAuth2Credentials.from_json(session['credentials'])
            if not credentials.access_token_expired:
                return redirect(url_for('internal_page.dashboard_page'))
            else:
                return render_template('index.html')
        else:
            return render_template('index.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('basic_page.er_page'))

@basic_page.route('/privacy-policy', methods=['GET'])
def pp_page():
    try:
        return render_template('privacy_policy.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('basic_page.er_page'))

@basic_page.route('/terms-conditions', methods=['GET'])
def tc_page():
    try:
        return render_template('terms_conditions.html')
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
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
            credentials = client.OAuth2Credentials.from_json(session['credentials'])
            # If credentials have expired refresh them
            if credentials.access_token_expired:
                client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret.json')
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
        return redirect(url_for('basic_page.er_page'))

@internal_page.route('/view-cards', methods=['GET'])
def vc_page():
    try:
        if 'credentials' not in session:
            return redirect(url_for('basic_page.la_page'))
        else:
            credentials = client.OAuth2Credentials.from_json(session['credentials'])

            # If credentials have expired refresh them
            if credentials.access_token_expired:
                client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret.json')
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
        return redirect(url_for('basic_page.er_page'))

@internal_page.route('/logout', methods=['GET'])
def lo_page():
    try:
        session.clear()
        return redirect(url_for('basic_page.la_page'))
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('basic_page.er_page'))


# GOOGLE API INTERACTIONS
@google_api.route('/process-login', methods=['GET', 'POST'])
def oauth2callback():
    try:
        client_secrets_path = os.path.join(current_app.root_path, 'static/data/private/client_secret.json')
        if 'credentials' not in session:
            flow = client.flow_from_clientsecrets(
                client_secrets_path,
                scope=scopes,
                redirect_uri=url_for('google_api.oauth2callback', _external=True))

            if 'code' not in request.args:
                auth_uri = flow.step1_get_authorize_url()
                return redirect(auth_uri)
            else:
                auth_code = request.args.get('code')
                credentials = flow.step2_exchange(auth_code)
                session['credentials'] = credentials.to_json()
                pl.process_login()
                return redirect(url_for('internal_page.dashboard_page'))

        credentials = client.OAuth2Credentials.from_json(session['credentials'])

        if credentials.access_token_expired:
            flow = client.flow_from_clientsecrets(
                client_secrets_path,
                scope=scopes,
                redirect_uri=url_for('google_api.oauth2callback', _external=True))

            if 'code' not in request.args:
                auth_uri = flow.step1_get_authorize_url()
                return redirect(auth_uri)
            else:
                auth_code = request.args.get('code')
                credentials = flow.step2_exchange(auth_code)
                session['credentials'] = credentials.to_json()
                return redirect(url_for('internal_page.dashboard_page'))
        else:
            return redirect(url_for('internal_page.dashboard_page'))
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('basic_page.er_page'))

@google_api.route('/get-sheets', methods=['GET', 'POST'])
def get_lists():
    try:
        # Determine request type
        inputs = json.loads(request.data)
        request_type = inputs['requestType']

        # Return Account Map and Selected Sheet ID (if it exists)
        if request_type == 'initial view':
            user_list = ps.get_user_sheets()
            public_list = ps.get_public_sheets()
            results = {"user_list": user_list, "public_list": public_list}
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
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('basic_page.er_page'))

@google_api.route('/save-sheet', methods=['GET', 'POST'])
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
        return redirect(url_for('basic_page.er_page'))

@google_api.route('/open-sheet', methods=['GET', 'POST'])
def open_sheet_permissions():
    try:
        if request.data is not None:
            inputs = json.loads(request.data)
            session.modified = True

            # Open sheet permissions
            ps.make_sheet_public(inputs['sheetID'])

        return jsonify({"status": "sheet shared"})
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return redirect(url_for('basic_page.er_page'))

@google_api.route('/card-data', methods=['GET'])
def output_card_data():
    try:
        results = cd.get_data()
        return jsonify(results)
    except:
        message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
            sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
        print(message)
        return message

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
#         message = "ERROR FOUND\nError Type: \"" + str(sys.exc_info()[0]) + "\"\nError Value: \"" + str(
#             sys.exc_info()[1]) + "\"\nError Traceback: \"" + str(sys.exc_info()[2]) + "\""
#         print(message)
#         return redirect(url_for('basic_page.er_page'))
