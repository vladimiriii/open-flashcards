# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, session, redirect, url_for, request
import os
import sys

# Custom Libraries
import app.lib.cardData as cd
import app.lib.processLogin as pl
import app.lib.processSheets as ps
from app.lib import utils

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'YES'

# Define the blueprint:
basic_page = Blueprint('basic_page', __name__)
internal_page = Blueprint('internal_page', __name__)
google_api = Blueprint('google_api', __name__)


# BASIC PAGES
@basic_page.route('/', methods=['GET'])
def landing_page():
    try:
        if 'credentials' in session:
            return redirect(url_for('internal_page.dashboard_page'))
        else:
            return render_template('index.html')
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/privacy-policy', methods=['GET'])
def pp_page():
    try:
        return render_template('privacy_policy.html')
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/terms-conditions', methods=['GET'])
def tc_page():
    try:
        return render_template('terms_conditions.html')
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/error', methods=['GET'])
def er_page():
    return render_template('error.html')


# GOOGLE API INTERACTIONS
@google_api.route('/process-login', methods=['GET'])
def start_login():
    try:
        authorization_url = pl.process_login()
        return redirect(authorization_url)
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/oauth2callback')
def oauth2callback():
    try:
        pl.handle_callback()
        pl.update_user_info()
        return redirect(url_for('internal_page.dashboard_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/flashcards/<sheet_id>')
def show_blog(sheet_id):
    try:
        if 'credentials' in session:
            permission_level = utils.check_user_role()
        else:
            permission_level = 'guest'

        return render_template('flashcards-template.html', sheet_id=sheet_id, permission_level=permission_level)
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


# LOGGED IN PAGES
@internal_page.route('/dashboard', methods=['GET'])
def dashboard_page():
    try:
        if 'credentials' in session:
            permission_level = utils.check_user_role()
            return render_template('dashboard.html', value=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/sheet-management')
def sheet_management_page():
    try:
        if 'credentials' in session:
            permission_level = utils.check_user_role()

            if permission_level == 'super_user':
                return render_template('sheet-management.html')
            else:
                return redirect(url_for('internal_page.dashboard_page'))

        else:
            return redirect(url_for('basic_page.landing_page'))

    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/user-management')
def user_management_page():
    try:
        if 'credentials' in session:
            permission_level = utils.check_user_role()

            if permission_level == 'super_user':
                return render_template('user-management.html')
            else:
                return redirect(url_for('internal_page.dashboard_page'))

        else:
            return redirect(url_for('basic_page.landing_page'))

    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/make-request')
def make_request_page():
    try:
        if 'credentials' in session:
            permission_level = utils.check_user_role()
            return render_template('make-request.html', value=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/logout', methods=['GET'])
def lo_page():
    try:
        session.clear()
        return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


# Card Creation Options
@internal_page.route('/create-flashcards', methods=['GET'])
def create_flashcards_page():
    try:
        if 'credentials' in session:
            permission_level = utils.check_user_role()
            return render_template('create-flashcards.html', permission_level=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/get-sheet-lists', methods=['GET'])
def get_sheet_lists():
    data_type = request.args['table']
    if data_type == "publicSheets":
        raw_data = ps.get_public_sheets()
    elif data_type == "userSheets" and 'au_id' in session:
        raw_data = ps.get_user_sheets(session['au_id'])
    elif data_type == "requestSheets" and 'au_id' in session:
        permission_level = utils.check_user_role()
        if permission_level == 'super_user':
            raw_data = ps.get_request_sheets()
    else:
        raw_data = None
    table_data = ps.process_sheet_data(raw_data)

    return jsonify(table_data)


# DATA ROUTES
@google_api.route('/register-sheet', methods=['POST'])
def register_sheet():
    google_id = request.data.decode('UTF-8')
    response = ps.import_new_sheet(google_id)

    return jsonify(response)


@google_api.route('/register-sheet-view', methods=['POST'])
def save_page():
    inputs = request.json
    ps.update_sheet_metadata(inputs['sheetID'])
    ps.add_sheet_view(inputs['sheetID'])

    return jsonify({"status": "Success"})


@google_api.route('/get-sheet-info', methods=['GET'])
def sheet_data():
    sheet_id = request.args['sheetId']
    google_id = cd.get_google_id(sheet_id)

    return jsonify({"googleId": google_id})


@google_api.route('/make-share-request', methods=['POST'])
def make_share_request():
    input = json.loads(request.data)
    google_id = input['googleId']
    result = ps.check_sheet_availability(google_id)
    if 'credentials' in session and result['status'] == 'sheet_accessible':
        permission_level = utils.check_user_role()
        if permission_level == 'super_user':
            ps.update_sheet_status(google_id, 3)
            result['status'] = 'sheet_made_public'
        else:
            ps.update_sheet_status(google_id, 2)

    return jsonify(result)


@google_api.route('/card-data', methods=['POST'])
def output_card_data():
    inputs = json.loads(request.data)
    sheet_id = inputs['sheetID']
    results = cd.get_data(sheet_id=sheet_id)

    return jsonify(results)
