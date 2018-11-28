# -*- coding: utf-8 -*-
import configparser
import os
from flask import Flask

# Custom Libraries
# import app.lib.database as dbse

def create_app():
    # Create the Flask app.
    app = Flask(__name__)

    # Load application configurations
    load_config(app)
    init_modules(app)

    return app

def init_modules(app):
    # Import a module / component using its blueprint handler variable
    from app.views import basic_page
    from app.views import google_api
    from app.views import internal_page

    # Register blueprint(s)
    app.register_blueprint(basic_page)
    app.register_blueprint(google_api)
    app.register_blueprint(internal_page)

# Read config file
def load_config(app):

    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    config = configparser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')
