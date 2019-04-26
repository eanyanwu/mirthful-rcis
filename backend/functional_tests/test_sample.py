import json

def test_unauthorized_login(client):
    response = login_as(client=client,
                        username='hacker',
                        password='pass')

    json_data = response.get_json()
    headers = response.headers

    assert response.status_code == 401
    assert "hacker doesn't exist" in json_data['error_message'] 
    assert headers.get('Set-Cookie', default=None) is None


def test_authorized_login(client, user_factory):
    # Setup
    user = setup_user(client, user_factory)

    response = login_as(client,
                        username=user['username'],
                        password=user['password'])

    headers = response.headers

    # assert that we got a `Set-Cookie` header
    assert headers.get('Set-Cookie', default=None) is not None

def test_create_and_read_rci(client, user_factory):
    # Setup 
    user = setup_user(client, user_factory)

    login_as(client,
             username=user['username'],
             password=user['password'])

    # Test 
    response = client.post('/api/rci')

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['user_id'] == user['user_id'] 

    # Since we are still logged in as the user
    # that created the rci, we should be able to read it
    rci_document_id = json_data['rci_document_id']

    response = client.get('/api/rci/{}'.format(rci_document_id))

    json_data = response.get_json()
    
    assert response.status_code == 200
    assert json_data['rci_document_id'] == rci_document_id





def login_as(client, username, password):
    response = client.post(
        '/login',
        data={
            'username': username,
            'password': password
        })

    return response

def setup_user(client, user_factory):
    with client.application.app_context():
        return user_factory()

