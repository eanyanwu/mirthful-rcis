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
