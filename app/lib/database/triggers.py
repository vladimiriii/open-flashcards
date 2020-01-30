from sqlalchemy import text


def sheet_action_update_trigger(db_session):
    trigger = text("""
        CREATE TRIGGER sheet_action_update
        AFTER INSERT
        ON sheet_action
        FOR EACH ROW
        EXECUTE PROCEDURE update_sheet_status();
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

    sheet_action_update_trigger(db_session)
