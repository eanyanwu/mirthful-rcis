from rci_response_utils import create_error_response

from flask import request
from functools import wraps

def is_valid_login(user_record, login_username, login_password):
    if not user_record:
        return False

    if 'username' not in user_record or 'password' not in user_record: 
        return False

    if user_record['username'] != login_username:
        return False

    # TODO: Hashing and salting can be done here
    return user_record['password'] == login_password

def login_required(func):
    # TODO: Explain the @wraps
    @wraps(func)
    def handle_authentication_check(*args, **kwargs):
        rci_session = request.cookies.get('rci_session')

        if not rci_session:
            return create_error_response('Unauthorized', 401)

        result = func(*args, **kwargs)

        return result

    return handle_authentication_check 
