from sqlalchemy import text


def sheet_action_trigger(db_session):
    trigger = text("""
        CREATE TRIGGER insert_on_sheet_action
        AFTER INSERT
        ON sheet_action
        FOR EACH ROW
        EXECUTE PROCEDURE update_sheet_status();
    """)

    db_session.execute(trigger)
    db_session.commit()


def app_user_action_trigger(db_session):
    trigger = text("""
        CREATE TRIGGER insert_on_app_user_action
        AFTER INSERT
        ON app_user_action
        FOR EACH ROW
        EXECUTE PROCEDURE update_app_user_role();
    """)

    db_session.execute(trigger)
    db_session.commit()


if __name__ == '__main__':
    from sqlalchemy.engine.url import URL
    from sqlalchemy.orm import scoped_session, sessionmaker
    from databaseConfig import DATABASE
    from sqlalchemy import create_engine

    engine = create_engine(URL(**DATABASE))
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=True,
                                             bind=engine))

    sheet_action_trigger(db_session)
    app_user_action_trigger(db_session)
