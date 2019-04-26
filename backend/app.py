import datastore 
import login
import rci

from authorization import authorize
from custom_exceptions import HttpRequestException, BadRequest, Unauthorized

import flask
import json
import uuid

from functools import wraps
from flask import Flask
from flask import request
from flask import json
from flask import g
from datetime import datetime, timedelta

app = Flask(__name__)


# PRE/POST REQUEST HOOKS
@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# DECORATORS
def login_required(func):
    # TODO: Explain the @wraps
    @wraps(func)
    def handle_authentication_check(*args, **kwargs):
        rci_session = request.cookies.get('session')

        if not rci_session:
            raise Unauthorized('Login required')

        result = func(*args, **kwargs)

        return result

    return handle_authentication_check 

## ERROR Handling
@app.errorhandler(HttpRequestException)
def handle_bad_request(error):
    response = flask.make_response(json.dumps(error.to_dict()))
    response.mimetype = 'application/json'
    response.status_code = error.status_code
    return response 
        
# ROUTING 
@app.route('/login', methods=['POST'])
def login_user():
    """
    Logs in a user by creating a new session for them in the database

    The session id is sent back in a cookie called `session`
    """
    username = request.form['username']
    password = request.form['password']

    if validate(username, password):
        session_id = start_session(username)

        extra_headers = { 'Set-Cookie': 'session={}'.format(session_id) }

        return create_json_response({}, 200, extra_headers)
    else:
        raise Unauthorized('Bad Login')

@app.route('/api/rci', methods=['POST'])
@login_required
def post_rci():
    """
    Create an empty Rci Document

    No authorization is needed here because any logged in user should
    be able to do this
    """
    session_id = request.cookies.get('session')

    user = get_session_user(session_id)

    new_rci = create_new_rci(user['user_id'])

    extra_headers = { 'Location': '/api/rci/' + new_rci['rci_document_id'] }

    return create_json_response(new_rci, 200, extra_headers) 

@app.route('/api/rci/<uuid:rci_id>', methods=['GET'])
@login_required
def get_rci(rci_id):
    """
    Return an already existing Rci Document if the user has access to it
    """
    user = get_session_user(request.cookies.get('session'))

    rci_doc = read_rci(str(rci_id), user['user_id'])
    
    return create_json_response(rci_doc, 200)

## LOGIC 

def validate(username, password):
    user_results = datastore.query('select * '
                                   'from users '
                                   'where username = ? '
                                   'limit 1;',
                                   (username,))

    user = next(iter(user_results), None)
    
    if user is None:
        raise Unauthorized("The user {} doesn't exist!".format(username))

    return login.is_valid_login(
        user,
        username,
        password)

def start_session(username):
    """
    Start a session for a given user
    """
    user_results = datastore.query('select * '
                                   'from users '
                                   'where username = ? '
                                   'limit 1;',
                                   (username,))

    user = next(iter(user_results), None)

    if user is None:
        raise BadRequest("The user {} doesn't exist!".format(username))

    session = login.create_session_obj(user['user_id'], 120)
   
    # The ** is for passing a dictionary as key-value arguments
    datastore.insert_session(**session)

    return session['session_id']

def get_session_user(session_id):
    """
    Fetch the user that is associated with a session 
    """

    session = datastore.select_session(session_id)

    if session is None:
        raise BadRequest('Invalid session {}'.format(session_id))

    user_id = session['user_id']

    user = datastore.select_user(user_id)

    if user is None:
        raise BadRequest('Invalid user {}'.format(user_id))

    return user

def read_rci(rci_id, user_id): 
    """
    Fetch a full rci document for the user

    The user is needed because rci's are protected resources
    The call will fail if the user is not authorized to read the document
    """
   
    # Collect the info we need to authorize
    rci = datastore.select_rci_document(rci_id)

    if rci is None:
        raise BadRequest('Invalid rci {}'.format(rci_id))
    
    user_roles = datastore.select_role_assignments(user_id)
    resource_acl_owners = datastore.select_rci_acl_owners(rci_id)
    resource_acl_groups = datastore.select_rci_acl_groups(rci_id)

    args = {
        'mode': 'r',
        'acs': rci['access_control'],
        'user_id': user_id,
        'user_roles': [x['user_id'] for x in user_roles],
        'resource_acl_owners': [x['acl_owner_id'] for x in resource_acl_owners],
        'resource_acl_groups': [x['acl_group_id'] for x in resource_acl_groups] 
    }

    authorize(**args)

    # If we get to this point, user is authorized


    # TODO: Craft the full rci document with damages coments and whatnot
    return rci

def create_new_rci(user_id):
    """
    Creates a new rci record and adds the user to the list of owners
    """

    args = {
        'rci_document_id': str(uuid.uuid4()),
        'user_id': user_id,
        'created_at': datetime.utcnow(),
        'access_control': 'o:rw;g:rw;w:__'
    }

    datastore.insert_rci_document(**args)

    datastore.insert_rci_document_acl_owner(
        rci_document_id=args['rci_document_id'],
        acl_owner_id=user_id)

    return args


## Utility Methods 

def create_error_response(message=None, 
                          status_code=None,
                          extra_headers=None):

    error = { 'error_message': message }

    if not status_code:
        status_code = 400

    return create_json_response(error, status_code, extra_headers)

def create_json_response(data=None, status_code=None, extra_headers=None):
    if not extra_headers:
        extra_headers = {}

    if not status_code:
        status_code = 200

    # Set the application/json mimetype
    extra_headers['Content-Type'] = 'application/json'

    return (json.dumps(data), status_code, extra_headers)

