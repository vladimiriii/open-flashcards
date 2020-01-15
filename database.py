import os
from datetime import datetime
import configparser

# SQL Alchemy
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

# Database Config
from app.lib.databaseConfig import DATABASE

# Database Models
from app.lib.models import Base, db_session, app_user_role, app_user, request_type

# ---------------------------------------------
# Steps to recreate database
# ---------------------------------------------
# DROP DATABASE openflashcards;
# CREATE DATABASE openflashcards;
# CREATE USER username WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE openflashcards TO username;


def create_user_roles():
    # Create Default User Roles
    role_1 = app_user_role(
        aur_role_name='super_user',
        aur_role_description="User plus the ability to moderate comments and ratings",
        aur_create_date=datetime.now(),
        aur_is_deleted=False
    )

    role_2 = app_user_role(
        aur_role_name='user',
        aur_role_description="Standard user, can view and import sheets",
        aur_create_date=datetime.now(),
        aur_is_deleted=False
    )

    role_3 = app_user_role(
        aur_role_name='guest_user',
        aur_role_description="Guest user, can only view public sheets",
        aur_create_date=datetime.now(),
        aur_is_deleted=False
    )

    db_session.add(role_1)
    db_session.add(role_2)
    db_session.add(role_3)
    db_session.flush()
    super_user_aur_id = role_1.aur_id
    guest_user_aur_id = role_3.aur_id

    db_session.commit()

    return super_user_aur_id, guest_user_aur_id


def create_request_types():

    # Create Default User Roles
    request_1 = request_type(
        rt_name='make_public',
        rt_description="User has requested to make the sheet available publically.",
        rt_create_date=datetime.now(),
        rt_last_modified=datetime.now()
    )

    db_session.add(request_1)
    db_session.commit()


def create_default_users(super_user_aur_id, guest_user_aur_id):
    app_dir = os.getcwd()
    config_filepath = app_dir + '/config.cfg'
    config = configparser.RawConfigParser()
    config.read(config_filepath)

    user_email = config.get('App_User_Account', 'USER_EMAIL')
    user_first_name = config.get('App_User_Account', 'USER_FIRST_NAME')
    user_last_name = config.get('App_User_Account', 'USER_LAST_NAME')

    user_1 = app_user(
        au_aur_id=super_user_aur_id,  # super user
        au_email=user_email,
        au_first_name=user_first_name,
        au_last_name=user_last_name,
        au_first_sign_in=datetime.now(),
        au_last_sign_in=datetime.now(),
        au_is_deleted=False
    )

    user_2 = app_user(
        au_aur_id=guest_user_aur_id,  # Normal user
        au_email=None,
        au_first_name='Guest',
        au_last_name='User',
        au_first_sign_in=datetime.now(),
        au_last_sign_in=datetime.now(),
        au_is_deleted=False
    )

    db_session.add(user_1)
    db_session.add(user_2)
    db_session.commit()


if __name__ == '__main__':

    try:
        engine = create_engine(URL(**DATABASE))
        Base.metadata.create_all(bind=engine)

        super_user_aur_id, guest_user_aur_id = create_user_roles()
        create_default_users(super_user_aur_id, guest_user_aur_id)
        create_request_types()

    except Exception as e:
        print(e)
