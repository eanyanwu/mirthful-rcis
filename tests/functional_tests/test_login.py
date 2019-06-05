import functools
import pytest

@pytest.mark.usefixtures('test_db')
def test_unauthorized_login(flask_client):
    fake_user = {
        'username': 'hacker',
        'password': 'pass'
    }
    response = flask_client.login_as(fake_user)

    json_data = response.get_json()
    headers = response.headers

    assert response.status_code == 401
    assert "Bad login" in json_data['error_message'] 
    assert headers.get('Set-Cookie', default=None) is None

@pytest.mark.usefixtures('test_db')
def test_login_logout(flask_client, student):
    # Test 
    response = flask_client.login_as(student)

    headers = response.headers

    json = response.get_json()

    # assert that we got a `Set-Cookie` header
    assert response.status_code == 200
    assert headers.get('Set-Cookie', default=None) is not None
    assert json['user_id'] == student['user_id']

    # logout
    response = flask_client.logout()

    assert response.status_code == 200

    # You need to be logged in to logout, so since we are
    # logged out, we shouldn't be able to logout again.

    response = flask_client.logout()

    assert response.status_code == 401

