# -*- coding: utf-8 -*-
from datetime import datetime
from flask import session

from app.lib.database.models import db_session, app_user, app_user_role, app_user_action, app_user_action_type
from app.lib.processLogin import get_profile_info


def update_user_info():
    profile_info = get_profile_info()
    email = profile_info['email']
    first_name = profile_info['given_name']
    last_name = profile_info['family_name']
    current_user = app_user.query.filter_by(au_email=email).first()

    if current_user is None:
        role_id = db_session.query(app_user_role.aur_id).filter_by(aur_role_name='Undergraduate').first()
        current_user = app_user(
            au_aur_id=role_id,
            au_email=email,
            au_first_name=first_name,
            au_last_name=last_name,
            au_created=datetime.utcnow(),
            au_last_modified=datetime.utcnow(),
        )
        db_session.add(current_user)
        db_session.commit()
    else:
        current_user.au_last_modified = datetime.utcnow()
        db_session.commit()

    session['au_id'] = current_user.au_id


def update_user_role(user_id, event):

    action_type_id = db_session.query(app_user_action_type.auat_id).filter_by(auat_type_name=event).scalar()

    new_event = app_user_action(
        aua_auat_id=action_type_id,
        aua_initiator_au_id=session['au_id'],
        aua_impacted_au_id=user_id,
        aua_timestamp=datetime.utcnow()
    )
    db_session.add(new_event)
    db_session.commit()

    new_status = (db_session.query(app_user_role.aur_role_name)
                            .filter(app_user.au_aur_id == app_user_role.aur_id)
                            .filter(app_user.au_id == user_id)
                            .first())

    return new_status
