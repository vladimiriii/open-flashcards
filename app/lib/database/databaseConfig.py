import os
import configparser

# Get Configuration Settings
par_dir = os.path.join(__file__, "../../..")
par_dir_abs_path = os.path.abspath(par_dir)
app_dir = os.path.dirname(par_dir_abs_path)
config_filepath = app_dir + '/config.cfg'

config = configparser.RawConfigParser()
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
