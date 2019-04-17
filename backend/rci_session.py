import uuid
from datetime import datetime
from datetime import timedelta

# Create new session object
def new(user_id, ttl_minutes=None):
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

