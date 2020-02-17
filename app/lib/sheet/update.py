# -*- coding: utf-8 -*-
from datetime import datetime
from flask import session

# Google API
from googleapiclient.errors import HttpError

# Custom Libraries
from app.lib.database.models import sheet, db_session, view, app_user, app_user_role, app_user_rel_sheet, sheet_status, sheet_action, sheet_action_type
import app.lib.user.extract as ue
import app.lib.sheet.extract as se


def add_new_sheet_entry(metadata):
    status_id = db_session.query(sheet_status.ss_id).filter_by(ss_status_name='Private').first()
    sheet_record = sheet(s_ss_id=status_id,
                         s_google_id=metadata['google_id'],
                         s_sheet_name=metadata['sheet_name'],
                         s_owner_name=metadata['owner_name'],
                         s_owner_email=metadata['owner_email'],
                         s_row_count=metadata['row_count'],
                         s_sheet_created=metadata['created_date'],
                         s_sheet_last_modified=metadata['last_modified'],
                         s_created=datetime.utcnow(),
                         s_last_modified=datetime.utcnow(),
                         )
    db_session.add(sheet_record)
    db_session.commit()

    return sheet_record.s_id


def add_new_user_rel_sheet_entry(sheet_id, is_owner):
    rel_record = app_user_rel_sheet(aurs_au_id=session['au_id'],
                                    aurs_s_id=sheet_id,
                                    aurs_first_view=datetime.now(),
                                    aurs_is_owner=is_owner,
                                    aurs_deleted=False)

    db_session.add(rel_record)
    db_session.commit()

    return rel_record.aurs_id


def update_sheet_metadata(sheet_id):

    google_id = db_session.query(sheet.s_google_id).filter_by(s_id=sheet_id).scalar()
    metadata = se.get_sheet_metadata(google_id)

    # Update sheet record with latest metadata
    sheet_record = sheet.query.filter_by(s_id=sheet_id).first()
    sheet_record.s_sheet_name = metadata['sheet_name']
    sheet_record.s_owner_name = metadata['owner_name']
    sheet_record.s_owner_email = metadata['owner_email']
    sheet_record.s_row_count = metadata['row_count']
    sheet_record.s_sheet_last_modified = metadata['last_modified']
    sheet_record.s_last_modifed = datetime.utcnow()

    # Commit changes to the database
    db_session.commit()


def add_sheet_view(sheet_id):
    if 'au_id' in session:
        view_record = view(v_au_id=session['au_id'],
                           v_s_id=sheet_id,
                           v_timestamp=datetime.now())
    else:
        guest_user_id = (db_session.query(app_user.au_id)
                                   .filter(app_user.au_aur_id == app_user_role.aur_id)
                                   .filter(app_user_role.aur_role_name == "Guest")
                                   .scalar())
        view_record = view(v_au_id=guest_user_id,
                           v_s_id=sheet_id,
                           v_timestamp=datetime.now())

    # Save to Database
    db_session.add(view_record)
    db_session.commit()

    return view_record.v_id


def import_new_sheet(google_id, user_role):
    response = {}
    current_sheet = sheet.query.filter_by(s_google_id=google_id).first()

    try:
        metadata = se.get_sheet_metadata(google_id)
        if current_sheet is None:
            if user_role == 'Undergraduate' and not metadata['is_owner']:
                response['status'] = 'upgrade_needed'
            else:
                sheet_id = add_new_sheet_entry(metadata)
                add_new_user_rel_sheet_entry(sheet_id, metadata['is_owner'])
                response['status'] = 'sheet_imported'
        else:
            sheet_id = current_sheet.s_id
            update_sheet_metadata(sheet_id)
            sheet_rel_user = app_user_rel_sheet.query.filter_by(aurs_s_id=sheet_id, aurs_au_id=session['au_id']).first()
            if user_role == 'Undergraduate' and not metadata['is_owner']:
                response['status'] = 'upgrade_needed'
            else:
                if sheet_rel_user is None:
                    add_new_user_rel_sheet_entry(sheet_id, metadata['is_owner'])
                    response['status'] = 'sheet_imported'
                else:
                    response['status'] = 'sheet_already_imported'

        response['sheetId'] = str(sheet_id)

    except HttpError as e:
        if e.resp.status == 404:
            response['status'] = 'sheet_not_exist'
        elif e.resp.status == 400:
            response['status'] = 'invalid_url'

    return response


def update_sheet_status(google_id, event):

    if event == 'Request Public':
        permission_level = ue.check_user_role()
        if permission_level == 'Super User':
            event = "Make Public"

    sheet_id = db_session.query(sheet.s_id).filter_by(s_google_id=google_id).scalar()
    action_type_id = db_session.query(sheet_action_type.sat_id).filter_by(sat_type_name=event).scalar()

    new_event = sheet_action(
        sa_au_id=session['au_id'],
        sa_s_id=sheet_id,
        sa_sat_id=action_type_id,
        sa_timestamp=datetime.utcnow()
    )
    db_session.add(new_event)
    db_session.commit()

    new_status = (db_session.query(sheet_status.ss_status_name)
                            .filter(sheet.s_ss_id == sheet_status.ss_id)
                            .filter(sheet.s_google_id == google_id)
                            .first())

    return new_status
