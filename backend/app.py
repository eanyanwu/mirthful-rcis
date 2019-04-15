import rci_datastore 
import rci_session 
import rci_login

from rci_response_utils import create_json_response
from rci_response_utils import create_error_response

import flask
from flask import Flask
from flask import request
from flask import json

app = Flask(__name__)



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # First make sure this is a valid user
    if validate(username, password):
        # If it is, create a session for them
        session_id = start_session(username)

        # Create the entry for the `Set-Cookie` header.
        # This will instruct the browser to set a cookie
        extra_headers = { 'Set-Cookie': 'rci_session=' + session_id }

        # Return basic information about the user
        user_info = get_user_info(username)
        
        return create_json_response(user_info, 200, extra_headers)
    else:
        # Bad login
        return create_error_response("Bad Login", 401)

@app.route('/', methods=['GET'])
@rci_login.login_required
def protected_route():
    return "You have reached a protected route"

def validate(username, password):
    return rci_login.is_valid_login(
        rci_datastore.get_user(username),
        username,
        password)


# Create a new session record in the database
def start_session(username):
    # First get the user record
    user = rci_datastore.get_user(username)

    # Use the user_id to create a new session
    session = rci_session.new(user['user_id'], 120)
    
    # Insert it into the database 
    rci_datastore.insert_session(session)

    return session['session_id']

# Simle method to extract the the info we need 
# out of a user database record
def get_user_info(username):
    user = rci_datastore.get_user(username)

    return { 'username' : user['username'] }

