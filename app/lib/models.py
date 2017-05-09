from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from app.lib.databaseConfig import DATABASE

# Create DB Engine
Base = declarative_base()
engine = create_engine(URL(**DATABASE))
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))

Base.query = db_session.query_property()

# Set Schema Name
schema_name = 'public'

# Create our database model
class app_user_role(Base):
    __tablename__ = 'app_user_role'
    __table_args__ = {"schema": schema_name}
    aur_id = Column(Integer, primary_key=True)
    aur_role_name = Column(String(120), unique=True)
    aur_role_description = Column(Text)
    aur_create_date = Column(DateTime)
    aur_is_deleted = Column(Boolean)

    def __init__(self, aur_role_name=None, aur_role_description=None, aur_create_date=None, aur_is_deleted=None):
        self.aur_role_name = aur_role_name
        self.aur_role_description = aur_role_description
        self.aur_create_date = aur_create_date
        self.aur_is_deleted = aur_is_deleted

class app_user(Base):
    __tablename__ = 'app_user'
    __table_args__ = {"schema": schema_name}
    au_id = Column(Integer, primary_key=True)
    au_aur_id = Column(Integer, ForeignKey(schema_name + '.app_user_role.aur_id'), nullable=False)
    au_email = Column(String(120), unique=True)
    au_first_name = Column(String(120), unique=True)
    au_last_name = Column(String(120), unique=True)
    au_gender = Column(String(12), unique=True)
    au_profile_url = Column(String(120), unique=True)
    au_first_sign_in = Column(DateTime)
    au_last_sign_in = Column(DateTime)
    au_is_deleted = Column(Boolean)

    def __init__(self,  au_aur_id=None, au_email=None, au_first_name=None, au_last_name=None, au_gender=None, au_profile_url=None, au_first_sign_in=None, au_last_sign_in=None, au_is_deleted=None):
        self.au_aur_id = au_aur_id
        self.au_email = au_email
        self.au_first_name = au_first_name
        self.au_last_name = au_last_name
        self.au_gender = au_gender
        self.au_first_sign_in = au_first_sign_in
        self.au_last_sign_in = au_last_sign_in
        self.au_is_deleted = au_is_deleted

class sheet(Base):
    __tablename__ = 'sheet'
    __table_args__ = {"schema": schema_name}
    s_id = Column(Integer, primary_key=True)
    s_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    s_ca_id = Column(Integer, ForeignKey(schema_name + '.category.ca_id'), nullable=False)
    s_sca_id = Column(Integer, ForeignKey(schema_name + '.subcategory.sca_id'), nullable=False)
    s_google_id = Column(String(120), unique=True)
    s_row_count = Column(Integer)
    s_last_modified = Column(DateTime)
    s_shared = Column(Boolean)
    s_date_shared = Column(DateTime)
    s_hide_sharer = Column(Boolean)

class comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {"schema": schema_name}
    c_id = Column(Integer, primary_key=True)
    c_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    c_s_id = Column(Integer, ForeignKey(schema_name + '.sheet.s_id'), nullable=False)
    c_text = Column(Text)
    c_date = Column(DateTime)
    c_comment_approved = Column(Boolean)
    c_is_deleted = Column(Boolean)

class rating(Base):
    __tablename__ = 'rating'
    __table_args__ = {"schema": schema_name}
    r_id = Column(Integer, primary_key=True)
    r_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    r_s_id = Column(Integer, ForeignKey(schema_name + '.sheet.s_id'), nullable=False)
    r_score = Column(Integer)
    r_create_date = Column(DateTime)
    r_is_deleted = Column(Boolean)

class view(Base):
    __tablename__ = 'view'
    __table_args__ = {"schema": schema_name}
    v_id = Column(Integer, primary_key=True)
    v_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    v_s_id = Column(Integer, ForeignKey(schema_name + '.sheet.s_id'), nullable=False)
    v_date = Column(DateTime)

class category(Base):
    __tablename__ = 'category'
    __table_args__ = {"schema": schema_name}
    ca_id = Column(Integer, primary_key=True)
    ca_cat_name = Column(String(120), unique=True)
    ca_cat_description = Column(Text)
    ca_create_date = Column(DateTime)
    ca_last_modified = Column(DateTime)

class subcategory(Base):
    __tablename__ = 'subcategory'
    __table_args__ = {"schema": schema_name}
    sca_id = Column(Integer, primary_key=True)
    sca_ca_id = Column(Integer, ForeignKey(schema_name + '.category.ca_id'), nullable=False)
    sca_cat_name = Column(String(120), unique=True)
    sca_cat_description = Column(Text)
    sca_create_date = Column(DateTime)
    sca_last_modified = Column(DateTime)
