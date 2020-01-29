from sqlalchemy import event, DDL


trig_ddl = DDL("""
    CREATE TRIGGER customers_search_vector_update BEFORE INSERT OR UPDATE
    ON customers
    FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(search_vector,'pg_catalog.english',customer_code,customer_name);
""")
tbl = Customer.__table__
event.listen(tbl, 'after_create', trig_ddl.execute_if(dialect='postgresql'))
