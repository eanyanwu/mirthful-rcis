from functional_tests.utils import login_as, setup_user

import json

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

def test_create_and_read_rci(client, user_factory):
    # Setup 
    user = setup_user(client, user_factory)
    login_as(user, client)

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


def test_create_rci_and_add_attachment(client, user_factory):
    # Setup 
    user = setup_user(client, user_factory)
    login_as(user, client)

    response = client.post('/api/rci')

    assert response.status_code == 200
    
    rci_document_id = response.get_json()['rci_document_id']

    # Test
    attachment = {
        'rci_attachment_type': 'TEXT',
        'content': {
            'url' : 'http://example.com',
            'text': 'A couple of scratches'
        }
    }

    response = client.post('/api/rci/{}/attachment'.format(rci_document_id),
                           json=attachment)

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['rci_attachment_type'] == 'TEXT'
    
def test_create_rci_and_try_to_add_attachment_by_unauthorized_user(client,
                                                               user_factory):
    user1 = setup_user(client, user_factory)
    user2 = setup_user(client, user_factory)

    login_as(user1, client)
    response = client.post('/api/rci')
    assert response.status_code == 200

    rci_document_id = response.get_json()['rci_document_id']

    # Now login as user2 and try to add a damage to that rci
    login_as(user2, client)
    attachment = {
        'rci_attachment_type': 'TEXT',
        'content' : {
            'details': 'This here is some content'
        }
    }

    response = client.post('/api/rci/{}/attachment'.format(rci_document_id),
                           json=attachment)

    json_data = response.get_json()
    print(json_data)
    assert response.status_code == 401
    assert 'you do not have sufficient permissions' in json_data['error_message'] 
    


