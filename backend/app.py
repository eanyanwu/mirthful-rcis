import rci_datastore 
import rci_session 
import rci_login
import rci
from rci_response_utils import create_json_response
from rci_response_utils import create_error_response

import flask
from flask import Flask
from flask import request
from flask import json

app = Flask(__name__)


# PRE/POST REQUEST HOOKS
@app.teardown_appcontext
def close_db_connection():
    if rci_datastore.__database is not None:
        rci_datastore.__database.close()


# ROUTING 

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if validate(username, password):
        session_id = start_session(username)

        extra_headers = { 'Set-Cookie': 'rci_session=' + session_id }

        user_info = get_user_info(username)
        
        return create_json_response(user_info, 200, extra_headers)
    else:
        return create_error_response("Bad Login", 401)

@app.route('/api/rci', methods=['POST'])
@rci_login.login_required
def create_new_rci():
    session_id = request.cookies.get('rci_session')
    session = rci_datastore.get_session(session_id)

    user_id = session['user_id']
    room_id = 'ROOM1'

    new_rci = rci.create_new_rci(user_id, room_id)

    extra_headers = { 'Location': '/api/rci/' + new_rci['rci_document_id'] }

    return create_json_response(new_rci, 200, extra_headers) 

@app.route('/api/rci/<uuid:rci_id>', methods=['GET'])
@rci_login.login_required
def fetch_rci(rci_id):
    result = rci.find_rci(str(rci_id))
    
    return create_json_response(result, 200)

def validate(username, password):
    return rci_login.is_valid_login(
        rci_datastore.get_user(username),
        username,
        password)


def start_session(username):
    user = rci_datastore.get_user(username)

    session = rci_session.new(user['user_id'], 120)
    
    rci_datastore.insert_session(session)

    return session['session_id']

def get_user_info(username):
    user = rci_datastore.get_user(username)

    return { 'username' : user['username'] }

