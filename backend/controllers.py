import rcicore as core
import authentication as auth
from app import app
from custom_exceptions import Unauthorized, BadRequest

import json
from flask import request
from flask import g

# ROUTING 
@app.route('/login', methods=['POST'])
def login_user():
    """
    Logs in a user by creating a new session for them in the database

    The session id is sent back in a cookie called `session`
    """
    username = request.form['username']
    password = request.form['password']

    if auth.validate(username, password):
        session_id = auth.start_session(username)

        extra_headers = { 'Set-Cookie': 'session={}'.format(session_id) }

        return create_json_response({}, 200, extra_headers)
    else:
        raise Unauthorized('Bad Login')

@app.route('/api/rci', methods=['POST'])
@auth.login_required
def post_rci():
    """
    Create an empty Rci Document

    No authorization is needed here because any logged in user should
    be able to do this
    """
    user = g.get('user')

    new_rci = core.post_rci(user['user_id'])

    extra_headers = { 'Location': '/api/rci/' + new_rci['rci_document_id'] }

    return create_json_response(new_rci, 200, extra_headers) 

@app.route('/api/rci/<uuid:rci_id>', methods=['GET'])
@auth.login_required
def get_rci(rci_id):
    """
    Return an already existing Rci Document if the user has access to it
    """
    user = g.get('user') 

    rci_doc = core.get_rci(str(rci_id), user['user_id'])
    
    return create_json_response(rci_doc, 200)

@app.route('/api/rci/<uuid:rci_id>/attachment', methods=['POST'])
@auth.login_required
def post_rci_attachment(rci_id):
    """
    Create a new attachment for the specified rci

    User will have to have read access to the rci document
    for this to work
    """
    user = g.get('user') 

    data = request.get_json()

    if data is None:
        # This means there was an error parsing it as json
        raise BadRequest('Malformed json {}'.format(request.data))

    rci_attachment = core.post_rci_attachment(str(rci_id), user['user_id'], data)

    return create_json_response(rci_attachment, 200)

@app.route('/api/rci/<uuid:rci_id>/attachment/<uuid:rci_attachment_id>',
           methods=['DELETE'])
@auth.login_required
def delete_rci_attachment(rci_id, rci_attachment_id):
    """
    Delete an rci attachment
    """

    user = g.get('user')

    core.delete_rci_attachment(str(rci_id),
                               str(rci_attachment_id), 
                               user['user_id'])

    return create_json_response({}, 200)

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

