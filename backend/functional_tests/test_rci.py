from functional_tests.utils import login_as 

import uuid
import json
import functools 

def test_try_read_nonexistent_rci(client, student):
    login_as(student, client)

    response = client.get('/api/rci/{}'.format(uuid.uuid4()))

    assert response.status_code == 400
    assert 'does not exist' in response.get_json()['error_message']

def test_create_rci_for_non_existent_room(client, student):
    room_id = uuid.uuid4()

    login_as(student, client)

    # Test
    response = client.post('/api/room/{}/rci'.format(room_id))

    assert response.status_code == 400
    assert 'does not exist' in response.get_json()['error_message']


def test_create_and_read_rci(client, student, room):
    # Setup 
    room_id = room['room_id']

    login_as(student, client)

    # Test 
    response = client.post('/api/room/{}/rci'.format(room_id))

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['room_id'] == room['room_id']

    rci_id = json_data['rci_id']

    response = client.get('/api/rci/{}'.format(rci_id))

    json_data = response.get_json()
    
    assert response.status_code == 200
    assert json_data['rci_id'] == rci_id 
    assert json_data['room_id'] == room_id 

def skip_test_add_attachment(client, user_factory, room_factory):
    # Setup 
    user = setup_user(client, user_factory)
    room = setup_room(client, room_factory)
    login_as(user, client)

    response = client.post('/api/rci', json={'room_id': room['room_id']})

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

def skip_test_delete_attachment(client, user_factory, room_factory):
    # Setup
    user = setup_user(client, user_factory)
    room = setup_room(client, room_factory)
    login_as(user, client)

    response = client.post('/api/rci', json={'room_id': room['room_id']})

    assert response.status_code == 200

    rci_document_id = response.get_json()['rci_document_id']

    attachment = {
        'rci_attachment_type': 'TEXT',
        'content': {}
    }

    response = client.post('/api/rci/{}/attachment'.format(rci_document_id),
                           json=attachment)

    assert response.status_code == 200

    attachment_id = response.get_json()['rci_attachment_id']

    # Test
    response = client.delete('/api/rci/{}/attachment/{}'
                             .format(rci_document_id, attachment_id))

    assert response.status_code == 200


    
def skip_test_add_attachment_by_unauthorized_user(client,
                                             user_factory,
                                             room_factory):
    user1 = setup_user(client, user_factory)
    user2 = setup_user(client, user_factory)
    room = setup_room(client, room_factory)

    login_as(user1, client)
    response = client.post('/api/rci',
                           json={'room_id': room['room_id']})
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

    assert response.status_code == 401
    assert 'you do not have sufficient permissions' in json_data['error_message'] 
    
def skip_test_try_delete_attachment_by_unauthorized_user(client,
                                                    user_factory,
                                                    room_factory):
    # Setup
    user1 = setup_user(client, user_factory)
    user2 = setup_user(client, user_factory)
    room = setup_room(client, room_factory)

    login_as(user1, client)

    response = client.post('/api/rci', json={'room_id': room['room_id']})

    rci_document_id = response.get_json()['rci_document_id']

    attachment = {
        'rci_attachment_type': 'TEXT',
        'content': {}
    }
    response = client.post('/api/rci/{}/attachment'.format(rci_document_id),
                           json=attachment)
    rci_attachment_id = response.get_json()['rci_attachment_id']

    # Test
    login_as(user2, client)
    response = client.delete('/api/rci/{}/attachment/{}'
                             .format(rci_document_id, rci_attachment_id))

    assert response.status_code == 401
