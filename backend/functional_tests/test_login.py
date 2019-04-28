from functional_tests.utils import login_as, setup_user

def test_unauthorized_login(client):
    fake_user = {
        'username': 'hacker',
        'password': 'pass'
    }
    response = login_as(fake_user, client)

    json_data = response.get_json()
    headers = response.headers

    assert response.status_code == 401
    assert "hacker doesn't exist" in json_data['error_message'] 
    assert headers.get('Set-Cookie', default=None) is None


def test_authorized_login(client, user_factory):
    # Setup
    user = setup_user(client, user_factory)
    response = login_as(user, client)

    headers = response.headers

    # assert that we got a `Set-Cookie` header
    assert headers.get('Set-Cookie', default=None) is not None

