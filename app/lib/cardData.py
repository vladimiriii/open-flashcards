# -*- coding: utf-8 -*-
from googleapiclient.errors import HttpError

from app.lib.database.models import db_session, sheet
from app.lib.errorLookup import error_lookup
from app.lib import utils


def get_data(sheet_id):
    google_id = get_google_id(sheet_id)

    if google_id is not None:
        service = utils.get_sheets_credentials()
        response = query_API(service=service, google_id=google_id)
        if 'error' not in response:
            final_data = process_data(response)
        else:
            final_data = response
    else:
        final_data = {'error': 'not_found'}

    return final_data


def get_google_id(sheet_id):

    google_id = db_session.query(sheet.s_google_id).filter_by(s_id=sheet_id).scalar()

    return google_id


def query_API(service, google_id):

    rangeName = 'A1:J'
    try:
        result = service.spreadsheets().values().get(spreadsheetId=google_id, range=rangeName).execute()
        values = result.get('values', [])
    except HttpError as err:
        if err.resp.status in error_lookup:
            values = {'error': error_lookup[err.resp.status]}
        else:
            values = {'error': error_lookup['other']}

    return values


def process_data(response):

    results = {}
    results['headers'] = response[0]
    results['data'] = response[1:len(response)]

    return results
