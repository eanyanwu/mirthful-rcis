import uuid
import json
import pytest

# Use the test_db fixture for all tests
pytestmark = pytest.mark.usefixtures('test_db')
 
def test_create_read_delete_rci(flask_client, student, room):
    # Setup 
    flask_client.login_as(student)
    
    # Create
    response = flask_client.create_rci(room)

    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data['room_name'] == room['room_name']
    assert json_data['building_name'] == room['building_name']
    

    rci_id = json_data['rci_id']
    
    # Read the rci by its id
    response = flask_client.get('/api/rcis/{}'.format(rci_id))

    json_data = response.get_json()
    
    assert response.status_code == 200
    assert json_data['rci_id'] == rci_id 
    assert json_data['room_name'] == room['room_name']
    assert json_data['building_name'] == room['building_name']

    # Read the rci by the user's id
    response = flask_client.get('/api/rcis?filter_type=USER_ID&filter_value={}'
                                .format(student['user_id']))

    json_data = response.get_json()
    
    assert response.status_code == 240
    assert len(json_data) == 1 # The user should only have one rci
    assert json_data[0]['rci_id'] == rci_id

    # Delete
    response = flask_client.delete('/api/rcis/{}'.format(rci_id))

    assert response.status_code == 200


def test_lock_unlock_rci(flask_client, res_life_staff, room):
    flask_client.login_as(res_life_staff)

    response = flask_client.create_rci(room)

    rci_id = response.get_json()['rci_id']
    
    # Lock it
    response = flask_client.post('/api/rcis/{}/lock'.format(rci_id))

    assert response.status_code == 200

    # Test that it cannot be edited
    response = flask_client.post('/api/rcis/{}/damages'.format(rci_id),
                                 json={
                                     'item': 'Wall',
                                     'text': 'Broken wall'
                                 })

    assert response.status_code == 400
    assert 'locked' in response.get_json()['error_message']

    # Unlock it 
    response = flask_client.delete('/api/rcis/{}/lock'.format(rci_id))

    assert response.status_code == 200

    # Test that it can now be edited
    response = flask_client.post('/api/rcis/{}/damages'.format(rci_id),
                                 json={
                                     'item': 'Wall',
                                     'text': 'Broken wall'
                                 })

    assert response.status_code == 200


def test_create_delete_damage(flask_client, student, room):
    flask_client.login_as(student)

    # Create Rci
    response = flask_client.create_rci(room)

    rci_id = response.get_json()['rci_id']

    assert response.status_code == 200
    assert len(response.get_json()['damages']) == 0

    # Add Damage
    response = flask_client.post('/api/rcis/{}/damages'.format(rci_id),
                                 json={
                                     'item': 'Walls',
                                     'text': 'Brokenk wall',
                                     'image_url': 'http://example.com'
                                 })
    
    assert response.status_code == 200
    
    damage_id = response.get_json()['damage_id']

    # Make sure that the damage was recorded
    response = flask_client.get('/api/rcis/{}'.format(rci_id))

    assert len(response.get_json()['damages']) == 1

    # Delete damage
    response = flask_client.delete('/api/rcis/{}/damages/{}'
                                   .format(rci_id, damage_id))

    assert response.status_code == 200
