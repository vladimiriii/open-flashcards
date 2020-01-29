import os
from datetime import datetime
import configparser

# SQL Alchemy
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

# Database
from app.lib.database.databaseConfig import DATABASE
from app.lib.database.models import Base, db_session, app_user_role, app_user, user_action_type, sheet_action_type, sheet_status, teacher_student_status

# ---------------------------------------------
# Steps to recreate database
# ---------------------------------------------
# DROP DATABASE openflashcards;
# CREATE DATABASE openflashcards;
# CREATE USER username WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE openflashcards TO username;


def create_user_roles():

    roles = [
        {"name": "Guest", "description": "User that has not logged in, can only view public sheets."},
        {"name": "Individual", "description": "Logged in user, can import and view their own sheets with restrictions."},
        {"name": "Self Learner", "description": "Logged in user. Can import and view their own sheets with no restrictions."},
        {"name": "Student", "description": "Logged in user that has been added by at least one Teacher. Can import and view own sheets with no restrictions, and view sheets imported by their Teacher(s)."},
        {"name": "Teacher", "description": "Logged in user. Can import and view their own sheets, plus add Students that will be able to view their sheets."},
        {"name": "Super User", "description": "Can import and view all sheets without restriction."}
    ]

    role_ids = {}
    for role in roles:
        role_entry = app_user_role(
            aur_role_name=role['name'],
            aur_role_description=role['description'],
            aur_created=datetime.now(),
            aur_last_modified=datetime.now()
        )
        db_session.add(role_entry)
        if role['name'] in ["Guest", "Super User"]:
            db_session.flush()
            role_ids[role['name']] = role_entry.aur_id

    db_session.commit()

    return role_ids


def create_default_users(role_ids):
    app_dir = os.getcwd()
    config_filepath = app_dir + '/config.cfg'
    config = configparser.RawConfigParser()
    config.read(config_filepath)

    user_email = config.get('App_User_Account', 'USER_EMAIL')
    user_first_name = config.get('App_User_Account', 'USER_FIRST_NAME')
    user_last_name = config.get('App_User_Account', 'USER_LAST_NAME')

    user_1 = app_user(
        au_aur_id=role_ids['Super User'],
        au_email=user_email,
        au_first_name=user_first_name,
        au_last_name=user_last_name,
        au_created=datetime.utcnow(),
        au_last_modified=datetime.utcnow(),
    )

    user_2 = app_user(
        au_aur_id=role_ids['Guest'],
        au_email=None,
        au_first_name='Guest',
        au_last_name='User',
        au_created=datetime.utcnow(),
        au_last_modified=datetime.utcnow(),
    )

    db_session.add(user_1)
    db_session.add(user_2)
    db_session.commit()


def create_user_action_type_defaults():

    action_types = [
        {"name": "Add Student", "description": "Add relationship between a Teacher user and a Student user."},
        {"name": "Remove Student", "description": "Remove a relationship between a Teacher user and a Student user."},
        {"name": "Change Role", "description": "Change the role of an existing user."},
        {"name": "Block", "description": "Blocks a user from logging in."}
    ]

    for action in action_types:
        action_entry = user_action_type(
            uat_type_name=action['name'],
            uat_type_description=action['description'],
            uat_created=datetime.utcnow(),
            uat_last_modified=datetime.utcnow()
        )
        db_session.add(action_entry)

    db_session.commit()


def create_teacher_student_status_defaults():

    statuses = [
        {"name": "Active", "description": "Relationship between the Teacher and the Student is active."},
        {"name": "Inactive", "description": "Relationship between the Teacher and the Student is inactive."}
    ]

    for status in statuses:
        status_entry = teacher_student_status(
            tss_status_name=status['name'],
            tss_status_description=status['description'],
            tss_created=datetime.utcnow(),
            tss_last_modified=datetime.utcnow()
        )
        db_session.add(status_entry)

    db_session.commit()


def create_sheet_status_defaults():

    statuses = [
        {"name": "Private", "description": "Sheet can only be seen by user who added the sheet."},
        {"name": "Public Review Requested", "description": "User has requested to make the sheet available publicly."},
        {"name": "Public", "description": "Sheet is viewable by all users."},
        {"name": "Deleted", "description": "Sheet has been deleted."},
    ]

    status_ids = {}
    for status in statuses:
        status_entry = sheet_status(
            ss_status_name=status['name'],
            ss_status_description=status['description'],
            ss_created=datetime.utcnow(),
            ss_last_modified=datetime.utcnow()
        )
        db_session.add(status_entry)
        db_session.flush()
        status_ids[status['name']] = status_entry.ss_id

    db_session.commit()

    return status_ids


def create_sheet_action_type_defaults(status_ids):

    action_types = [
        {
            "name": "Import",
            "description": "Import sheet details into database.",
            "start_ss_id": None,
            "end_ss_id": status_ids['Private']
        },
        {
            "name": "Request Public",
            "description": "User has requested to make the sheet available publicly.",
            "start_ss_id": status_ids['Private'],
            "end_ss_id": status_ids['Public Review Requested']
        },
        {
            "name": "Make Public",
            "description": "Make a sheet publicly available.",
            "start_ss_id": status_ids['Public Review Requested'],
            "end_ss_id": status_ids['Public']
        },
        {
            "name": "Make Private",
            "description": "Make a sheet private.",
            "start_ss_id": status_ids['Public'],
            "end_ss_id": status_ids['Private']
        },
        {
            "name": "Delete",
            "description": "Delete the sheet from the app.",
            "start_ss_id": None,
            "end_ss_id": status_ids['Deleted']
        }
    ]

    for action in action_types:
        action_entry = sheet_action_type(
            sat_type_name=action['name'],
            sat_type_description=action['description'],
            sat_start_ss_id=action['start_ss_id'],
            sat_end_ss_id=action['end_ss_id'],
            sat_created=datetime.utcnow(),
            sat_last_modified=datetime.utcnow()
        )
        db_session.add(action_entry)

    db_session.commit()


if __name__ == '__main__':

    engine = create_engine(URL(**DATABASE))
    Base.metadata.create_all(bind=engine)

    role_ids = create_user_roles()
    create_default_users(role_ids)
    create_user_action_type_defaults()
    create_teacher_student_status_defaults()
    status_ids = create_sheet_status_defaults()
    create_sheet_action_type_defaults(status_ids)
