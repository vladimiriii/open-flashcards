#! /usr/bin/env bash
echo `python3 -m venv env`
currentDir=`pwd`
virtualenvPath='env/bin/activate'
source $currentDir/$virtualenvPath

echo "Installing requirements..."
pip3 install -r requirements.txt
echo "Installation complete."
