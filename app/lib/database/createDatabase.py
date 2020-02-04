import os
from datetime import datetime
import configparser

# SQL Alchemy
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

# Database
from databaseConfig import DATABASE
from models import Base, db_session, app_user_role, app_user, app_user_action_type, sheet_action_type, sheet_status, student_sheet_status
from procedures import update_sheet_status_procedure, update_app_user_role_procedure
from triggers import sheet_action_update_trigger, app_user_role_update_trigger

# ---------------------------------------------
# Steps to recreate database
# ---------------------------------------------
# DROP DATABASE openflashcards;
# CREATE DATABASE openflashcards;
# CREATE USER username WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE openflashcards TO username;


def create_app_user_roles():
    roles = [
        {"name": "Guest", "description": "User that has not logged in, can only view public sheets."},
        {"name": "Undergraduate", "description": "Logged in user, can import and view their own sheets with restrictions."},
        {"name": "Graduate", "description": "Logged in user. Can import and view their own sheets with no restrictions."},
        {"name": "Professor", "description": "Logged in user. Can import and view their own sheets, plus add other users that will be able to view their sheets."},
        {"name": "Super User", "description": "Can import and view all sheets without restriction."},
        {"name": "Blocked", "description": "User is not allowed to access the App."}
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
        db_session.flush()
        role_ids[role['name']] = role_entry.aur_id

    db_session.commit()

    return role_ids


def create_default_app_users(role_ids):
    # Get Configuration Settings
    par_dir = os.path.join(__file__, "../../..")
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)
    config = configparser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
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


def create_app_user_action_type_defaults(role_ids):
    action_types = [
        {
            "name": "Bought Graduate Package",
            "description": "Upgrades an individual to allow unrestricted access.",
            "start_aur_id": role_ids["Undergraduate"],
            "end_aur_id": role_ids["Graduate"]
        },
        {
            "name": "Graduate Package Expired",
            "description": "User access to Graduate features has expired.",
            "start_aur_id": role_ids["Graduate"],
            "end_aur_id": role_ids["Undergraduate"]
        },
        {
            "name": "Bought Professor Package",
            "description": "Upgrades any user to a Professor.",
            "start_aur_id": None,
            "end_aur_id": role_ids["Professor"]
        },
        {
            "name": "Professor Package Expired",
            "description": "User access to Professor features has expired.",
            "start_aur_id": role_ids["Professor"],
            "end_aur_id": role_ids["Undergraduate"]
        },
        {
            "name": "Block User",
            "description": "Blocks a user from logging in.",
            "start_aur_id": None,
            "end_aur_id": role_ids["Blocked"]
        }
    ]

    for action in action_types:
        action_entry = app_user_action_type(
            auat_type_name=action['name'],
            auat_type_description=action['description'],
            auat_start_aur_id=action['start_aur_id'],
            auat_end_aur_id=action['end_aur_id'],
            auat_created=datetime.utcnow(),
            auat_last_modified=datetime.utcnow()
        )
        db_session.add(action_entry)

    db_session.commit()


def create_student_sheet_status_defaults():
    statuses = [
        {"name": "Active", "description": "Student access to the sheet is active."},
        {"name": "Inactive", "description": "Student access to the sheet is inactive."}
    ]

    for status in statuses:
        status_entry = student_sheet_status(
            sss_status_name=status['name'],
            sss_status_description=status['description'],
            sss_created=datetime.utcnow(),
            sss_last_modified=datetime.utcnow()
        )
        db_session.add(status_entry)

    db_session.commit()


def create_sheet_status_defaults():
    statuses = [
        {"name": "Private", "description": "Sheet can only be seen by user who added the sheet."},
        {"name": "Review Requested", "description": "User has requested to make the sheet available publicly."},
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
            "name": "Request Public",
            "description": "User has requested to make the sheet available publicly.",
            "start_ss_id": status_ids['Private'],
            "end_ss_id": status_ids['Review Requested']
        },
        {
            "name": "Approve Sheet",
            "description": "Sheet has been approved to be publicly available.",
            "start_ss_id": status_ids['Review Requested'],
            "end_ss_id": status_ids['Public']
        },
        {
            "name": "Make Public",
            "description": "Sheet has been made publicly available without a review.",
            "start_ss_id": status_ids['Private'],
            "end_ss_id": status_ids['Public']
        },
        {
            "name": "Cancel Request",
            "description": "The request to review the sheet has been cancelled.",
            "start_ss_id": status_ids['Review Requested'],
            "end_ss_id": status_ids['Private']
        },
        {
            "name": "Make Private",
            "description": "Sheet has been made private.",
            "start_ss_id": status_ids['Public'],
            "end_ss_id": status_ids['Private']
        },
        {
            "name": "Delete",
            "description": "Sheet has been deleted.",
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

    role_ids = create_app_user_roles()
    create_default_app_users(role_ids)
    create_app_user_action_type_defaults(role_ids)
    create_student_sheet_status_defaults()
    status_ids = create_sheet_status_defaults()
    create_sheet_action_type_defaults(status_ids)

    update_sheet_status_procedure(db_session)
    sheet_action_update_trigger(db_session)
    update_app_user_role_procedure(db_session)
    app_user_role_update_trigger(db_session)
