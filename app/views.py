# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, json, render_template, session, redirect, url_for, request
import os
import sys

# Custom Libraries
import app.lib.cardData as cd
import app.lib.processLogin as pl
import app.lib.sheet.extract as se
import app.lib.sheet.update as su
import app.lib.user.extract as ue
import app.lib.user.update as uu
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
        if 'credentials' in session:
            permission_level = ue.check_user_role()
        else:
            permission_level = 'Guest'
        return render_template('privacy_policy.html', value=permission_level)
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/terms-conditions', methods=['GET'])
def tc_page():
    try:
        if 'credentials' in session:
            permission_level = ue.check_user_role()
        else:
            permission_level = 'Guest'
        return render_template('terms_conditions.html', value=permission_level)
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
        uu.update_user_info()
        return redirect(url_for('internal_page.dashboard_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@basic_page.route('/flashcards/<sheet_id>')
def show_blog(sheet_id):
    try:
        if 'credentials' in session:
            permission_level = ue.check_user_role()
        else:
            permission_level = 'Guest'

        return render_template('flashcards-template.html', sheet_id=sheet_id, permission_level=permission_level)
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


# LOGGED IN PAGES
@internal_page.route('/dashboard', methods=['GET'])
def dashboard_page():
    try:
        if 'credentials' in session:
            permission_level = ue.check_user_role()
            return render_template('dashboard.html', value=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/student-management')
def student_management_page():
    try:
        if 'credentials' in session:
            permission_level = ue.check_user_role()
            if permission_level in ['Teacher', 'Super User']:
                return render_template('student-management.html', value=permission_level)
            else:
                return redirect(url_for('internal_page.dashboard_page'))
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/sheet-management')
def sheet_management_page():
    try:
        if 'credentials' in session:
            permission_level = ue.check_user_role()
            if permission_level == 'Super User':
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
            permission_level = ue.check_user_role()
            if permission_level == 'Super User':
                return render_template('user-management.html')
            else:
                return redirect(url_for('internal_page.dashboard_page'))
        else:
            return redirect(url_for('basic_page.landing_page'))

    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@internal_page.route('/upgrade')
def upgrade_page():
    try:
        if 'credentials' in session:
            permission_level = ue.check_user_role()
            return render_template('upgrade.html', value=permission_level)
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
            permission_level = ue.check_user_role()
            return render_template('create-flashcards.html', value=permission_level)
        else:
            return redirect(url_for('basic_page.landing_page'))
    except:
        print(utils.generate_error_message(sys.exc_info()))
        return redirect(url_for('basic_page.er_page'))


@google_api.route('/get-sheet-lists', methods=['GET'])
def get_sheet_lists():
    data_type = request.args['table']
    if data_type == "publicSheets":
        raw_data = se.get_public_sheets()
    elif data_type == "userSheets" and 'au_id' in session:
        raw_data = se.get_user_sheets(session['au_id'])
    elif data_type == "requestSheets" and 'au_id' in session:
        permission_level = ue.check_user_role()
        if permission_level == 'Super User':
            raw_data = se.get_request_sheets()
    else:
        raw_data = None

    table_data = utils.process_table_data(raw_data)

    return jsonify(table_data)


@google_api.route('/get-student-list', methods=['GET'])
def get_student_list():
    if 'au_id' in session:
        permission_level = ue.check_user_role()
        if permission_level in ['Super User', 'Teacher']:
            raw_data = ue.get_student_data(session['au_id'])
        else:
            raw_data = None
    else:
        raw_data = None

    table_data = utils.process_table_data(raw_data)

    return jsonify(table_data)


@google_api.route('/get-user-list', methods=['GET'])
def get_user_list():
    if 'au_id' in session:
        permission_level = ue.check_user_role()
        if permission_level == 'Super User':
            raw_data = ue.get_user_data()
        else:
            raw_data = None
    else:
        raw_data = None

    table_data = utils.process_table_data(raw_data)

    return jsonify(table_data)


# DATA ROUTES
@google_api.route('/register-sheet', methods=['POST'])
def register_sheet():
    if 'au_id' in session:
        user_role = ue.check_user_role()
        google_id = request.data.decode('UTF-8')
        response = su.import_new_sheet(google_id, user_role)
    else:
        response = 'unknown_error'
    return jsonify(response)


@google_api.route('/register-sheet-view', methods=['POST'])
def save_page():
    inputs = request.json
    su.update_sheet_metadata(inputs['sheetID'])
    su.add_sheet_view(inputs['sheetID'])

    return jsonify({"status": "Success"})


@google_api.route('/get-sheet-info', methods=['GET'])
def sheet_data():
    sheet_id = request.args['sheetId']
    google_id = cd.get_google_id(sheet_id)

    return jsonify({"googleId": google_id})


@google_api.route('/update-sheet-status', methods=['POST'])
def process_update_sheet_status_request():
    input = json.loads(request.data)
    google_id = input['googleId']
    event = input['event']

    result = se.check_sheet_availability(google_id)
    if 'credentials' in session and result['status'] == 'sheet_accessible':
        result['status'] = su.update_sheet_status(google_id=google_id, event=event)

    return jsonify(result)


@google_api.route('/update-user-role', methods=['POST'])
def process_update_user_role_request():
    input = json.loads(request.data)
    user_id = int(input['userId'])
    event = input['event']

    result = {}
    if 'au_id' in session:
        permission_level = ue.check_user_role()
        if permission_level == 'Super User':
            result['event'] = uu.update_user_role(user_id=user_id, event=event)
        else:
            result['event'] = "Unauthorized Access"
    else:
        result['event'] = "Unauthorized Access"

    return jsonify(result)


@google_api.route('/card-data', methods=['POST'])
def output_card_data():
    inputs = json.loads(request.data)
    sheet_id = inputs['sheetID']
    if 'au_id' in session:
        user_has_access = se.check_user_has_access(sheet_id, session['au_id'])
        if user_has_access:
            results = cd.get_data(sheet_id=sheet_id)
        else:
            results = {'error': 'incorrect_premissions'}
    else:
        sheet_is_public = se.check_sheet_is_public(sheet_id)
        if sheet_is_public:
            results = cd.get_data(sheet_id=sheet_id)
        else:
            results = {'error': 'incorrect_premissions'}

    return jsonify(results)
