# -*- coding: utf-8 -*-
from app.lib.database.models import db_session


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
