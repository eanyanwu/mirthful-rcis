import rci_session

import pytest

from datetime import timedelta


def test_call_fails_when_user_id_is_None():
    with pytest.raises(ValueError):
        rci_session.new(None)

def test_new_session_is_created_with_default_ttl_60_minutes():
    new_session = rci_session.new(123)
    ttl = new_session['expires_at'] - new_session['created_at']
    assert ttl == timedelta(minutes=60)
    assert new_session['user_id'] == 123

def test_new_session_is_created_with_custom_ttl():
    new_session = rci_session.new(123, 120)

    ttl = new_session['expires_at'] - new_session['created_at']
    assert ttl == timedelta(minutes=120)
    assert new_session['user_id'] == 123
