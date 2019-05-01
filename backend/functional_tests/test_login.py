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
    assert "hacker doesn't exist" in json_data['error_message'] 
    assert headers.get('Set-Cookie', default=None) is None

@pytest.mark.usefixtures('test_db')
def test_authorized_login(flask_client, student):
    # Test 
    response = flask_client.login_as(student)

    headers = response.headers

    # assert that we got a `Set-Cookie` header
    assert headers.get('Set-Cookie', default=None) is not None

