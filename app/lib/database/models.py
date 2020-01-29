from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from app.lib.database.databaseConfig import DATABASE
# from app.lib.database import triggers

# Create DB Engine
Base = declarative_base()
engine = create_engine(URL(**DATABASE))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))

Base.query = db_session.query_property()
schema_name = 'public'


# Create our database model
class app_user_role(Base):
    __tablename__ = 'app_user_role'
    __table_args__ = {"schema": schema_name}
    aur_id = Column(Integer, primary_key=True)
    aur_role_name = Column(String(120))
    aur_role_description = Column(Text)
    aur_created = Column(DateTime)
    aur_last_modified = Column(DateTime)

    def __init__(self,
                 aur_role_name=None,
                 aur_role_description=None,
                 aur_created=None,
                 aur_last_modified=None):
        self.aur_role_name = aur_role_name
        self.aur_role_description = aur_role_description
        self.aur_created = aur_created
        self.aur_last_modified = aur_last_modified


class app_user(Base):
    __tablename__ = 'app_user'
    __table_args__ = {"schema": schema_name}
    au_id = Column(Integer, primary_key=True)
    au_aur_id = Column(Integer, ForeignKey(schema_name + '.app_user_role.aur_id'), nullable=False)
    au_email = Column(String(120))
    au_first_name = Column(String(120))
    au_last_name = Column(String(120))
    au_created = Column(DateTime)
    au_last_modified = Column(DateTime)

    def __init__(self,
                 au_aur_id=None,
                 au_email=None,
                 au_first_name=None,
                 au_last_name=None,
                 au_created=None,
                 au_last_modified=None):
        self.au_aur_id = au_aur_id
        self.au_email = au_email
        self.au_first_name = au_first_name
        self.au_last_name = au_last_name
        self.au_created = au_created
        self.au_last_modified = au_last_modified


class teacher_rel_student(Base):
    __tablename__ = 'teacher_rel_student'
    __table_args__ = {"schema": schema_name}
    trs_id = Column(Integer, primary_key=True)
    trs_teacher_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    trs_student_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    trs_status = Column(Integer, ForeignKey(schema_name + '.teacher_student_status.tss_id'), nullable=False)
    trs_created = Column(DateTime)
    trs_last_modified = Column(DateTime)

    def __init__(self,
                 trs_id=None,
                 trs_teacher_au_id=None,
                 trs_student_au_id=None,
                 trs_status=None,
                 trs_created=None,
                 trs_last_modified=None):
        self.trs_id = trs_id
        self.trs_teacher_au_id = trs_teacher_au_id
        self.trs_student_au_id = trs_student_au_id
        self.trs_status = trs_status
        self.trs_created = trs_created
        self.trs_last_modified = trs_last_modified


class teacher_student_status(Base):
    __tablename__ = 'teacher_student_status'
    __table_args__ = {"schema": schema_name}
    tss_id = Column(Integer, primary_key=True)
    tss_status_name = Column(String(120))
    tss_status_description = Column(Text)
    tss_created = Column(DateTime)
    tss_last_modified = Column(DateTime)

    def __init__(self,
                 tss_status_name=None,
                 tss_status_description=None,
                 tss_created=None,
                 tss_last_modified=None):
        self.tss_status_name = tss_status_name
        self.tss_status_description = tss_status_description
        self.tss_created = tss_created
        self.tss_last_modified = tss_last_modified


class user_action(Base):
    __tablename__ = 'user_action'
    __table_args__ = {"schema": schema_name}
    ua_id = Column(Integer, primary_key=True)
    ua_uat_id = Column(Integer, ForeignKey(schema_name + '.user_action_type.uat_id'), nullable=False)
    ua_initiator_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    ua_impacted_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    ua_timestamp = Column(DateTime)

    def __init__(self,
                 ua_uat_id=None,
                 ua_initiator_au_id=None,
                 ua_impacted_au_id=None,
                 ua_timestamp=None):
        self.ua_uat_id = ua_uat_id
        self.ua_initiator_au_id = ua_initiator_au_id
        self.ua_impacted_au_id = ua_impacted_au_id
        self.ua_timestamp = ua_timestamp


class user_action_type(Base):
    __tablename__ = 'user_action_type'
    __table_args__ = {"schema": schema_name}
    uat_id = Column(Integer, primary_key=True)
    uat_type_name = Column(String(120))
    uat_type_description = Column(Text)
    uat_created = Column(DateTime)
    uat_last_modified = Column(DateTime)

    def __init__(self,
                 uat_type_name=None,
                 uat_type_description=None,
                 uat_created=None,
                 uat_last_modified=None):
        self.uat_type_name = uat_type_name
        self.uat_type_description = uat_type_description
        self.uat_created = uat_created
        self.uat_last_modified = uat_last_modified


class sheet(Base):
    __tablename__ = 'sheet'
    __table_args__ = {"schema": schema_name}
    s_id = Column(Integer, primary_key=True)
    s_ss_id = Column(Integer, ForeignKey(schema_name + '.sheet_status.ss_id'), nullable=False)
    s_google_id = Column(String(120), index=True)
    s_sheet_name = Column(Text)
    s_owner_name = Column(Text)
    s_owner_email = Column(Text)
    s_row_count = Column(Integer)
    s_created = Column(DateTime)
    s_last_modified = Column(DateTime)

    def __init__(self,
                 s_ss_id=None,
                 s_google_id=None,
                 s_sheet_name=None,
                 s_owner_name=None,
                 s_owner_email=None,
                 s_row_count=None,
                 s_created=None,
                 s_last_modified=None):
        self.s_ss_id = s_ss_id
        self.s_google_id = s_google_id
        self.s_sheet_name = s_sheet_name
        self.s_owner_name = s_owner_name
        self.s_owner_email = s_owner_email
        self.s_row_count = s_row_count
        self.s_created = s_created
        self.s_last_modified = s_last_modified


class view(Base):
    __tablename__ = 'view'
    __table_args__ = {"schema": schema_name}
    v_id = Column(Integer, primary_key=True)
    v_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    v_s_id = Column(Integer, ForeignKey(schema_name + '.sheet.s_id'), nullable=False)
    v_timestamp = Column(DateTime)

    def __init__(self,
                 v_au_id=None,
                 v_s_id=None,
                 v_timestamp=None):
        self.v_au_id = v_au_id
        self.v_s_id = v_s_id
        self.v_timestamp = v_timestamp


class sheet_status(Base):
    __tablename__ = 'sheet_status'
    __table_args__ = {"schema": schema_name}
    ss_id = Column(Integer, primary_key=True)
    ss_status_name = Column(String(120))
    ss_status_description = Column(Text)
    ss_created = Column(DateTime)
    ss_last_modified = Column(DateTime)

    def __init__(self,
                 ss_status_name=None,
                 ss_status_description=None,
                 ss_created=None,
                 ss_last_modified=None):
        self.ss_status_name = ss_status_name
        self.ss_status_description = ss_status_description
        self.ss_created = ss_created
        self.ss_last_modified = ss_last_modified


class sheet_action(Base):
    __tablename__ = 'sheet_action'
    __table_args__ = {"schema": schema_name}
    sa_id = Column(Integer, primary_key=True)
    sa_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    sa_s_id = Column(Integer, ForeignKey(schema_name + '.sheet.s_id'), nullable=False)
    sa_sat_id = Column(Integer, ForeignKey(schema_name + '.sheet_action_type.sat_id'), nullable=False)
    sa_timestamp = Column(DateTime)

    def __init__(self,
                 sa_sat_id=None,
                 sa_au_id=None,
                 sa_s_id=None,
                 sa_timestamp=None):
        self.sa_au_id = sa_au_id
        self.sa_s_id = sa_s_id
        self.sa_sat_id = sa_sat_id
        self.sa_timestamp = sa_timestamp


class sheet_action_type(Base):
    __tablename__ = 'sheet_action_type'
    __table_args__ = {"schema": schema_name}
    sat_id = Column(Integer, primary_key=True)
    sat_type_name = Column(String(120))
    sat_type_description = Column(Text)
    sat_start_ss_id = Column(Integer, ForeignKey(schema_name + '.sheet_status.ss_id'), nullable=True)
    sat_end_ss_id = Column(Integer, ForeignKey(schema_name + '.sheet_status.ss_id'), nullable=False)
    sat_created = Column(DateTime)
    sat_last_modified = Column(DateTime)

    def __init__(self,
                 sat_type_name=None,
                 sat_type_description=None,
                 sat_start_ss_id=None,
                 sat_end_ss_id=None,
                 sat_created=None,
                 sat_last_modified=None):
        self.sat_type_name = sat_type_name
        self.sat_type_description = sat_type_description
        self.sat_start_ss_id = sat_start_ss_id
        self.sat_end_ss_id = sat_end_ss_id
        self.sat_created = sat_created
        self.sat_last_modified = sat_last_modified


class app_user_rel_sheet(Base):
    __tablename__ = 'app_user_rel_sheet'
    __table_args__ = {"schema": schema_name}
    aurs_id = Column(Integer, primary_key=True)
    aurs_au_id = Column(Integer, ForeignKey(schema_name + '.app_user.au_id'), nullable=False)
    aurs_s_id = Column(Integer, ForeignKey(schema_name + '.sheet.s_id'), nullable=False)
    aurs_first_view = Column(DateTime)
    aurs_is_owner = Column(Boolean)
    aurs_deleted = Column(Boolean)
    aurs_created = Column(DateTime)
    aurs_last_modified = Column(DateTime)

    def __init__(self,
                 aurs_au_id=None,
                 aurs_s_id=None,
                 aurs_first_view=None,
                 aurs_is_owner=None,
                 aurs_deleted=None,
                 aurs_created=None,
                 aurs_last_modified=None):
        self.aurs_au_id = aurs_au_id
        self.aurs_s_id = aurs_s_id
        self.aurs_first_view = aurs_first_view
        self.aurs_is_owner = aurs_is_owner
        self.aurs_deleted = aurs_deleted
        self.aurs_created = aurs_created
        self.aurs_last_modified = aurs_last_modified
