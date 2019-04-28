import authentication

import pytest
from datetime import timedelta

# Is Valid Login Tests 
def test_no_user_record_is_provided():
    result = authentication.is_valid_login(None, 'username', 'password')
    assert result == False


def test_badly_formated_user_record():
    result = authentication.is_valid_login(
        { 'random': 'property' },
        'sally',
        '123')
    
    assert result == False

def test_user_record_username_does_not_match():
    result = authentication.is_valid_login(
        { 
            'username' : 'sally',
            'password' : '123'
        },
        'bob',
        '123')

    assert result == False

def test_user_record_password_does_not_match():
    result = authentication.is_valid_login(
        {
            'username' : 'sally',
            'password' : '123'
        },
        'sally',
        '203880')

    assert result == False

def test_valid_login():
    result = authentication.is_valid_login(
        {
            'username': 'sally',
            'password': '123'
        },
        'sally',
        '123')

    assert result == True

    
# Create Sesssion Obj Tests 

def test_create_session_fails_when_user_id_is_None():
    with pytest.raises(ValueError):
        authentication.create_session_obj(None)

def test_new_session_is_created_with_default_ttl_60_minutes():
    new_session = authentication.create_session_obj(123)
    ttl = new_session['expires_at'] - new_session['created_at']

    assert ttl == timedelta(minutes=60)
    assert new_session['user_id'] == 123

def test_new_session_is_created_with_custom_ttl():
    new_session = authentication.create_session_obj(123, 120)
    ttl = new_session['expires_at'] - new_session['created_at']

    assert ttl == timedelta(minutes=120)
    assert new_session['user_id'] == 123
