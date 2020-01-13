import os
from datetime import datetime
import configparser

# SQL Alchemy
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

# Database Config
from app.lib.databaseConfig import DATABASE

# Database Models
import app.lib.models as md

# ---------------------------------------------
# Steps to recreate database
# ---------------------------------------------
# DROP DATABASE openflashcards;
# CREATE DATABASE openflashcards;
# CREATE USER username WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE openflashcards TO username;


def create_user_roles(eng):
    # Create Tables
    md.Base.metadata.create_all(bind=engine)

    # Create Default User Roles
    insert1 = md.app_user_role.__table__.insert().values(
        aur_role_name='super_user',
        aur_role_description="User plus the ability to moderate comments and ratings",
        aur_create_date=datetime.now(),
        aur_is_deleted=False
    )

    insert2 = md.app_user_role.__table__.insert().values(
        aur_role_name='user',
        aur_role_description="Standard user, can view and import sheets",
        aur_create_date=datetime.now(),
        aur_is_deleted=False
    )

    eng.execute(insert1)
    eng.execute(insert2)


def create_request_types(eng):
    # Create Tables
    md.Base.metadata.create_all(bind=engine)

    # Create Default User Roles
    insert1 = md.request_type.__table__.insert().values(
        rt_name='make_public',
        rt_description="User has requested to make the sheet available publically.",
        rt_create_date=datetime.now(),
        rt_last_modified=datetime.now()
    )

    eng.execute(insert1)


def create_default_users(eng):
    app_dir = os.getcwd()
    config_filepath = app_dir + '/config.cfg'
    config = configparser.RawConfigParser()
    config.read(config_filepath)

    user_email = config.get('App_User_Account', 'USER_EMAIL')
    user_first_name = config.get('App_User_Account', 'USER_FIRST_NAME')
    user_last_name = config.get('App_User_Account', 'USER_LAST_NAME')

    insert3 = md.app_user.__table__.insert().values(
        au_aur_id=1,  # super user
        au_email=user_email,
        au_first_name=user_first_name,
        au_last_name=user_last_name,
        au_first_sign_in=datetime.now(),
        au_last_sign_in=datetime.now(),
        au_is_deleted=False
    )

    insert4 = md.app_user.__table__.insert().values(
        au_aur_id=2,  # Normal user
        au_email=None,
        au_first_name='Guest',
        au_last_name='User',
        au_first_sign_in=datetime.now(),
        au_last_sign_in=datetime.now(),
        au_is_deleted=False
    )

    eng.execute(insert3)
    eng.execute(insert4)


if __name__ == '__main__':

    try:
        engine = create_engine(URL(**DATABASE))
        create_user_roles(engine)
        create_request_types(engine)
        create_default_users(engine)
    except Exception as e:
        print(e)

