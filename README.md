# README

A flashcards application that allows you to use Google Sheets to generate Flashcards.

## Installation

1. Create a new empty PostgreSQL database.
2. Copy config-template.cfg to config.cfg.
3. Fill in the required fields in config.cfg.
4. Run `bash install.sh` to install requirements.
5. Get Google API client secrets file and copy to folder app/static/data/private/
6. Activate the virtualenv `. venv/bin/activate`
7. Run `python database.py` to create the required tables in the database. This file can also be used to drop all the tables if needed.

## Run

1. Run `bash run.sh`
