import uuid
from datetime import datetime
from datetime import timedelta

# Create new session object
def new(user_id, ttl_minutes=60):
    now = datetime.utcnow()

    return { 
        'session_id': str(uuid.uuid4()),
        'user_id': user_id,
        'created_at': now,
        'expires_at': now + timedelta(minutes=ttl_minutes)
    }

