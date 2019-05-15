import pytest

pytestmark = pytest.mark.usefixtures('test_db')

def test_get_all_rooms(flask_client, student, room):
    flask_client.login_as(student)

    response = flask_client.get('/api/rooms')

    rooms = response.get_json()

    print(rooms)

    assert response.status_code == 200
    
    # The room that we got via fixture should be one of the ones present
    bldg = room['building_name']
    assert any(x['room_name'] == room['room_name']  and 
               x['building_name'] == room['building_name']
               for x in rooms[bldg])

