from app import create_error_response
from app import create_json_response

import json

# create_error_response tests
def test_create_error_response_defaults():
    data, status_code, headers = create_error_response()
    json_data = json.loads(data)
    assert json_data['error_message'] == None
    assert status_code == 400
    assert headers['Content-Type'] == 'application/json' 

def test_create_error_response_different_status_code():
    __, status_code, __ = create_error_response(status_code=401)

    assert status_code == 401

def test_create_error_response_custom_message():
    data, __, __ = create_error_response(message='Error')

    json_data = json.loads(data)

    assert json_data['error_message'] == 'Error'

def test_create_error_response_additional_header():
    __, __, headers = create_error_response(
        extra_headers={ 'Set-Cookie': 'name=eze' })

    assert headers['Set-Cookie'] == 'name=eze'
                        

# create_json_response tests    
def test_create_json_response_defaults():
    data, status_code, headers = create_json_response()
    
    json_data = json.loads(data)

    assert json_data == None
    assert status_code == 200
    assert headers['Content-Type'] == 'application/json'

def test_create_json_response_different_status_code():
    __, status_code, __ = create_json_response(status_code=201)

    assert status_code == 201

def test_create_json_response_custom_message():
    data, __, __ = create_json_response(data={'Test': 'Value'})

    json_data = json.loads(data)

    assert json_data['Test'] == 'Value'

def test_create_json_response_additional_headers():
    __, __, headers = create_json_response(
        extra_headers={'Extra': 'Header'})

    assert headers['Extra'] == 'Header'
