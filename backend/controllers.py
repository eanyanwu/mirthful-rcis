import rcicore as core
import authentication as auth
from app import app
from custom_exceptions import Unauthorized, BadRequest

import json
import uuid
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

@app.route('/api/room/<uuid:room_id>/rci', methods=['POST'])
@auth.login_required
def post_rci(room_id):
    """
    Create an empty Rci Document for a room

    No authorization is needed here because any logged in user should
    be able to do this
    """
    user = g.get('user')
    
    room_id = str(room_id)

    new_rci = core.post_rci(user_id=user['user_id'],
                            room_id=room_id)

    return create_json_response(new_rci, 200, {}) 

@app.route('/api/rci/<uuid:rci_id>', methods=['GET'])
@auth.login_required
def get_rci(rci_id):
    """
    Return an existing rci
    """

    rci = core.get_rci(str(rci_id))
    
    return create_json_response(rci, 200)

@app.route('/api/rci/<uuid:rci_id>/damage', methods=['POST'])
@auth.login_required
def post_damage(rci_id):
    """
    Record a damage on the rci
    """
    user = g.get('user') 
    rci_id = str(rci_id)
    data = request.get_json()

    if data is None:
        raise BadRequest('Malformed json {}'.format(request.data))

    text = data.get('text', None)
    url = data.get('image_url', None)

    if text is None:
        raise BadRequest('damage text is None')

    damage = core.post_damage(user, rci_id, text, url)

    return create_json_response(damage, 200)

@app.route('/api/rci/<uuid:rci_id>/damage/<uuid:damage_id>', methods=['DELETE'])
@auth.login_required
def delete_damage(rci_id, damage_id):
    """
    Delete an rci attachment
    """

    user = g.get('user')
    rci_id = str(rci_id)
    damage_id = str(damage_id)

    core.delete_damage(rci_id, damage_id, user)

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

