# -*- coding: utf-8 -*-
from flask import session

from app.lib.database.models import db_session, app_user, app_user_role


def get_student_data(au_id):
    query = (f"""
        SELECT au_id,
            aur_role_name,
            au_email,
            CONCAT(au_first_name, ' ', au_last_name) AS au_full_name,
            au_created,
            au_last_modified
        FROM app_user
        INNER JOIN app_user_role
        ON au_aur_id = aur_id
        WHERE au_id = {au_id}
        """)

    data = db_session.execute(query)
    return data


def get_user_data():
    query = ("""
        SELECT au_id,
            aur_role_name,
            au_email,
            CONCAT(au_first_name, ' ', au_last_name) AS au_full_name,
            au_created,
            au_last_modified
        FROM app_user
        INNER JOIN app_user_role
        ON au_aur_id = aur_id
        """)

    data = db_session.execute(query)
    return data


def check_user_role(au_id):
    user_role = (db_session.query(app_user, app_user_role)
                           .filter(app_user.au_id == au_id)
                           .filter(app_user.au_aur_id == app_user_role.aur_id)
                           .first()).app_user_role.aur_role_name

    return user_role


def check_user_role_by_email(email):
    user_role = (db_session.query(app_user, app_user_role)
                           .filter(app_user.au_email == email)
                           .filter(app_user.au_aur_id == app_user_role.aur_id)
                           .first()).app_user_role.aur_role_name

    return user_role
