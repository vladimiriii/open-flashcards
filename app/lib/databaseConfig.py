import os
import configparser

# CREATE DATABASE openflashcards;
# CREATE USER username WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE openflashcards TO username;
# SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'
# DROP TABLE comment; DROP TABLE rating; DROP TABLE view;  DROP TABLE sheet; DROP TABLE app_user; DROP TABLE app_user_role; DROP TABLE subcategory; DROP TABLE category;

# Get Configuration Settings
par_dir = os.path.join(__file__, "../..")
par_dir_abs_path = os.path.abspath(par_dir)
app_dir = os.path.dirname(par_dir_abs_path)
config = configparser.RawConfigParser()
config_filepath = app_dir + '/config.cfg'
config.read(config_filepath)

DB_PORT = config.get('Database', 'DB_PORT')
DB_HOST = config.get('Database', 'DB_HOST')
DB_NAME = config.get('Database', 'DB_NAME')
DB_USERNAME = config.get('Database', 'DB_USERNAME')
DB_PASSWORD = config.get('Database', 'DB_PASSWORD')

DATABASE = {
    'drivername': 'postgres',
    'host': DB_HOST,
    'port': DB_PORT,
    'username': DB_USERNAME,
    'password': DB_PASSWORD,
    'database': DB_NAME
}
