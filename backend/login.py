import uuid
from datetime import datetime
from datetime import timedelta

from flask import request

def is_valid_login(user_record, login_username, login_password):
    if not user_record:
        return False

    if 'username' not in user_record or 'password' not in user_record: 
        return False

    if user_record['username'] != login_username:
        return False

    # TODO: Hashing and salting can be done here
    return user_record['password'] == login_password


# Create new session object
def create_session_obj(user_id, ttl_minutes=None):
    if not ttl_minutes:
        ttl_minutes = 60

    # Make sure user_id is not null
    if not user_id:
        raise ValueError("user_id is None")

    now = datetime.utcnow()

    return { 
        'session_id': str(uuid.uuid4()),
        'user_id': user_id,
        'created_at': now,
        'expires_at': now + timedelta(minutes=ttl_minutes)
    }
