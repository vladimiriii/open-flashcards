from sqlalchemy import text


def update_sheet_status_procedure(db_session):

    procedure = text("""
    CREATE OR REPLACE FUNCTION update_sheet_status() RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        DECLARE
            current_status INTEGER;
            next_status INTEGER;
        BEGIN

            SELECT INTO current_status s_ss_id
            FROM sheet
            WHERE s_id = NEW.sa_s_id;

            SELECT INTO next_status sat_end_ss_id
            FROM sheet_action_type
            WHERE sat_id = NEW.sa_sat_id
            AND (sat_start_ss_id = current_status
                OR sat_start_ss_id IS NULL);

            UPDATE sheet
            SET s_ss_id = next_status
                , s_last_modified = CURRENT_TIMESTAMP
            WHERE s_id = NEW.sa_s_id;

            RETURN NULL;
        END;
        $$;
    """)

    db_session.execute(procedure)
    db_session.commit()


def update_app_user_role_procedure(db_session):

    procedure = text("""
    CREATE OR REPLACE FUNCTION update_app_user_role() RETURNS TRIGGER
        LANGUAGE plpgsql
        AS $$
        DECLARE
            current_role INTEGER;
            next_role INTEGER;
        BEGIN

            SELECT INTO current_role au_aur_id
            FROM app_user
            WHERE au_id = NEW.au_aur_id;

            SELECT INTO next_role auat_end_aur_id
            FROM app_user_action_type
            WHERE auat_id = NEW.aua_auat_id
            AND (auat_start_aur_id = current_role
                OR auat_start_aur_id IS NULL);

            UPDATE app_user
            SET au_aur_id = next_role
                , au_last_modified = CURRENT_TIMESTAMP
            WHERE au_id = NEW.au_aur_id;

            RETURN NULL;
        END;
        $$;
    """)

    db_session.execute(procedure)
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

    update_sheet_status_procedure(db_session)
    update_app_user_role_procedure(db_session)
