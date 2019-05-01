from custom_exceptions import HttpRequestException 

import flask
import json
from flask import Flask
from flask import g

app = Flask(__name__)

import controllers

# PRE/POST REQUEST HOOKS
@app.teardown_appcontext
def close_db_connection(exception):
    db = g.get('_database', None)
    if db is not None:
        db.close()


## ERROR HANDLING
@app.errorhandler(HttpRequestException)
def handle_bad_request(error):
    response = flask.make_response(json.dumps(error.to_dict()))
    response.mimetype = 'application/json'
    response.status_code = error.status_code
    return response 
        


