from mirthful_rcis.lib import authentication

import pytest
from datetime import timedelta

# Test that login sets the cookie
# Test that logout deletes the session and redirects 
def test_login_logout(auth, dashboard):
    response = auth.login()

    assert response.headers['Set-Cookie'] is not None
    assert 'session=' in response.headers['Set-Cookie']
    assert 'Path=/' in response.headers['Set-Cookie']

    response = auth.logout()

    # Logout should redirect us 
    assert response.status_code == 302

    # Since no user is logged in, this should redirect us back to the login
    # page
    response = dashboard.main()

    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location'] 


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
