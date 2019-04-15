from rci_response_utils import create_error_response

from flask import request

# Validate a login attempt
def is_valid_login(user_record, login_username, login_password):
    if not user_record:
        # No user record was given.
        # This would happen if no record was found matching
        # the username
        return False

    # If the user record does not have the properties we are looking for
    if 'username' not in user_record or 'password' not in user_record: 
        return False

    if user_record['username'] != login_username:
        return False

    # TODO: Hashing and salting can be done here
    return user_record['password'] == login_password

# Decorator function for asserting that a particalar path
# can't be accessed unless user is logged in
def login_required(func):
    def wrapping_method(*args, **kwargs):
        rci_session = request.cookies.get('rci_session')

        if not rci_session:
            return create_error_response('Unauthorized', 401)

        result = func()

        return result

    return wrapping_method 
