# -*- coding: utf-8 -*-
import config

DB_PORT = config.DB_PORT
DB_HOST = config.DB_HOST
DB_NAME = config.DB_NAME
DB_USERNAME = config.DB_USERNAME
DB_PASSWORD = config.DB_PASSWORD

DATABASE = {
    'drivername': 'postgres',
    'host': DB_HOST,
    'port': DB_PORT,
    'username': DB_USERNAME,
    'password': DB_PASSWORD,
    'database': DB_NAME
}
