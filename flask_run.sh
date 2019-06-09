#!/bin/sh

source ./venv/bin/activate
export FLASK_APP=mirthful_rcis
export FLASK_ENV=development
flask run --host=0.0.0.0
