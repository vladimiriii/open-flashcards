from datetime import datetime

# SQL Alchemy
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine

# Database Config
from app.lib.databaseConfig import DATABASE

# Database Models
import app.lib.models as md

# Creates the DB engine
engine = create_engine(URL(**DATABASE))

# Drop Old Tables
drop_query = ('DROP TABLE app_user_rel_sheet; '
              'DROP TABLE subcategory; '
              'DROP TABLE category; '
              'DROP TABLE rating; '
              'DROP TABLE comment; '
              'DROP TABLE view; '
              'DROP TABLE sheet; '
              'DROP TABLE app_user; '
              'DROP TABLE app_user_role;')
engine.execute(drop_query)
md.Base.metadata.drop_all(bind=engine)

# Create New Tables
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

engine.execute(insert1)
engine.execute(insert2)

# TODO: Add insert for admin users (i.e. me)
