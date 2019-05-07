import uuid
import json
import pytest

# Use the test_db fixture for all tests
pytestmark = pytest.mark.usefixtures('test_db')
 
def test_try_read_nonexistent_rci(flask_client, student):
    flask_client.login_as(student)

    response = flask_client.get('/api/rci/{}'.format(uuid.uuid4()))

    assert response.status_code == 400
    assert 'does not exist' in response.get_json()['error_message']

def test_try_create_rci_for_non_existent_room(flask_client, student):
    room_id = uuid.uuid4()

    flask_client.login_as(student)

    # Test
    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    assert response.status_code == 400
    assert 'does not exist' in response.get_json()['error_message']


def test_create_read_delete_rci(flask_client, student, room):
    # Setup 
    room_id = room['room_id']

    flask_client.login_as(student)
    
    # Create
    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['room_id'] == room['room_id']
    

    rci_id = json_data['rci_id']
    
    # Read the rci by its id
    response = flask_client.get('/api/rci/{}'.format(rci_id))

    json_data = response.get_json()
    
    assert response.status_code == 200
    assert json_data['rci_id'] == rci_id 
    assert json_data['room_id'] == room_id 

    # Read the rci by the user's id
    response = flask_client.get('/api/user/{}/rcis'.format(student['user_id']))

    json_data = response.get_json()

    assert response.status_code == 200
    assert len(json_data) == 1 # The user should only have one rci
    assert json_data[0]['rci_id'] == rci_id

    # Delete
    response = flask_client.delete('/api/rci/{}'.format(rci_id))

    assert response.status_code == 200


def test_lock_unlock_rci(flask_client, res_life_staff, room):
    room_id = room['room_id']

    flask_client.login_as(res_life_staff)

    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    rci_id = response.get_json()['rci_id']
    
    # Lock it
    response = flask_client.post('/api/rci/{}/lock'.format(rci_id))

    assert response.status_code == 200

    # Test that it cannot be edited
    response = flask_client.post('/api/rci/{}/damage'.format(rci_id),
                                 json={
                                     'item': 'Wall',
                                     'text': 'Broken wall'
                                 })

    assert response.status_code == 400
    assert 'locked' in response.get_json()['error_message']

    # Unlock it 
    response = flask_client.delete('/api/rci/{}/lock'.format(rci_id))

    assert response.status_code == 200

    # Test that it can now be edited
    response = flask_client.post('/api/rci/{}/damage'.format(rci_id),
                                 json={
                                     'item': 'Wall',
                                     'text': 'Broken wall'
                                 })

    assert response.status_code == 200


def test_try_record_damage_without_text(flask_client, student, room):
    room_id = room['room_id']

    flask_client.login_as(student)

    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    rci_id = response.get_json()['rci_id']

    response = flask_client.post('/api/rci/{}/damage'.format(rci_id),
                                 json={'item': 'Desk'})

    assert response.status_code == 400
    assert 'damage text is None' in response.get_json()['error_message']

def test_try_record_damage_on_non_existing_rci(flask_client, student, room):
    room_id = room['room_id']
    fake_rci_id = str(uuid.uuid4())

    flask_client.login_as(student)

    response = flask_client.post('/api/rci/{}/damage'.format(fake_rci_id),
                                 json={
                                     'item': 'Wall',
                                     'text': 'Broken wall'
                                 })

    assert response.status_code == 400
    assert 'does not exist' in response.get_json()['error_message']

def test_create_delete_damage(flask_client, student, room):
    room_id = room['room_id']
    
    flask_client.login_as(student)

    # Create Rci
    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    rci_id = response.get_json()['rci_id']

    assert response.status_code == 200
    assert len(response.get_json()['damages']) == 0

    # Add Damage
    response = flask_client.post('/api/rci/{}/damage'.format(rci_id),
                                 json={
                                     'item': 'Walls',
                                     'text': 'Brokenk wall',
                                     'image_url': 'http://example.com'
                                 })
    
    assert response.status_code == 200
    
    damage_id = response.get_json()['damage_id']

    # Make sure that the damage was recorded
    response = flask_client.get('/api/rci/{}'.format(rci_id))

    assert len(response.get_json()['damages']) == 1

    # Delete damage
    response = flask_client.delete('/api/rci/{}/damage/{}'
                                   .format(rci_id, damage_id))

    assert response.status_code == 200


def test_add_damage_to_rci_by_res_life_staff(flask_client,
                                             student,
                                             res_life_staff,
                                             room):
    room_id = room['room_id']

    flask_client.login_as(student)

    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    rci_id = response.get_json()['rci_id']

    # Now login as a res_life_staff member and add damages
    flask_client.login_as(res_life_staff)

    response = flask_client.post('/api/rci/{}/damage'.format(rci_id),
                                 json={
                                     'item': 'Desk',
                                     'text': 'You forgot this damage'
                                 })

    assert response.status_code == 200

def test_try_add_damage_by_unauthorized_user(flask_client,
                                             user_factory,
                                             room):
    room_id = room['room_id']

    # Create the original owner of the rci
    student_1 = user_factory('student')

    flask_client.login_as(student_1)

    response = flask_client.post('/api/room/{}/rci'.format(room_id))

    rci_id = response.get_json()['rci_id']

    # Now login as the second user, a student who should
    # not have access to this rci
    student_2 = user_factory('student')
    flask_client.login_as(student_2)

    response = flask_client.post('/api/rci/{}/damage'.format(rci_id),
                                 json={
                                     'item': 'Bed',
                                     'text': 'Broken bed'
                                 })

    assert response.status_code == 401
    assert 'cannot record damage' in response.get_json()['error_message']


    
