import os
import sys
from datetime import datetime
import configparser
from pathlib import Path

# SQL Alchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database Config
from app.lib.databaseConfig import DATABASE

# Database Models
import app.lib.models as md

# Creates the DB engine
engine = create_engine(URL(**DATABASE))

# Drop Old Tables
drop_query = ( 'DROP TABLE app_user_rel_sheet; '
               'DROP TABLE subcategory; '
               'DROP TABLE category; '
               'DROP TABLE rating; '
               'DROP TABLE comment; '
               'DROP TABLE view; '
               'DROP TABLE sheet; '
               'DROP TABLE app_user; '
               'DROP TABLE app_user_role;')
engine.execute(drop_query)
md.Base.metadata.drop_all(bind=engine)#, tables=[md.subcategory, md.category, md.rating, md.comment, md.view, md.sheet, md.app_user, md.app_user_role])

# Create New Tables
md.Base.metadata.create_all(bind=engine)

# Create Default User Roles
insert1 = md.app_user_role.__table__.insert().values(
    aur_role_name = 'super_user',
    aur_role_description = "User plus the ability to moderate comments and ratings",
    aur_create_date = datetime.now(),
    aur_is_deleted = False
    )

insert2 = md.app_user_role.__table__.insert().values(
    aur_role_name = 'user',
    aur_role_description = "Standard user, can view and import sheets",
    aur_create_date = datetime.now(),
    aur_is_deleted = False
    )

engine.execute(insert1)
engine.execute(insert2)
