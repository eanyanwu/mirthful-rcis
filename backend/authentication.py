import datastore
from custom_exceptions import Unauthorized, BadRequest

import uuid
from datetime import datetime
from datetime import timedelta
from functools import wraps
from flask import request
from flask import g

def login_required(func):
    # TODO: Explain the @wraps
    @wraps(func)
    def handle_authentication_check(*args, **kwargs):
        rci_session = request.cookies.get('session')

        if not rci_session:
            raise Unauthorized('Login required')

        # Add the usre to the flask context global so that downstream
        # methods can easily access it 
        load_logged_in_user(session_id=rci_session)

        result = func(*args, **kwargs)

        return result

    return handle_authentication_check 

def load_logged_in_user(session_id):
    user = get_session_user(session_id=session_id)
    g.user = user

def get_session_user(session_id):
    """
    Fetch the user that is associated with a session 
    """

    user = datastore.query('select u.* '
                           'from sessions as s '
                           'inner join users as u '
                           'on s.user_id = u.user_id '
                           'where s.session_id = :session_id '
                           'limit 1; ',
                           { 'session_id': session_id },
                           one=True)

    if user is None:
        raise BadRequest('Could not find user for session {}'
                         .format(session_id))

    return user


def validate(username, password):
    user = datastore.query('select * '
                           'from users '
                           'where username = ? '
                           'limit 1;',
                           (username,),
                           one=True)
    
    if user is None:
        raise Unauthorized("The user {} doesn't exist!".format(username))

    return is_valid_login(user, username, password)

def is_valid_login(user_record, login_username, login_password):
    if user_record is None:
        return False

    if 'username' not in user_record or 'password' not in user_record: 
        return False

    if user_record['username'] != login_username:
        return False

    # TODO: Hashing and salting can be done here
    return user_record['password'] == login_password



def start_session(username):
    """
    Start a session for a given user
    """
    user = datastore.query('select * '
                           'from users '
                           'where username = ? '
                           'limit 1;',
                           (username,),
                           one=True)

    if user is None:
        raise BadRequest("The user {} doesn't exist!".format(username))

    s = create_session_obj(user['user_id'], 120)
   
    datastore.query('insert into '
                    'sessions (session_id, user_id, created_at, expires_at) '
                    'values (:session_id, :user_id, :created_at, :expires_at)',
                    s)
    

    return s['session_id']

def create_session_obj(user_id, ttl_minutes=None):
    if ttl_minutes is None:
        ttl_minutes = 60

    # Make sure user_id is not null
    if user_id is None:
        raise ValueError("user_id is None")

    now = datetime.utcnow()

    return { 
        'session_id': str(uuid.uuid4()),
        'user_id': user_id,
        'created_at': now,
        'expires_at': now + timedelta(minutes=ttl_minutes)
    }
