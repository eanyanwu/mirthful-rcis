import json


def create_error_response(message=None, 
                          status_code=None,
                          extra_headers=None):

    error = { 'error_message': message }

    if not status_code:
        status_code = 400

    return create_json_response(error, status_code, extra_headers)

def create_json_response(data=None, status_code=None, extra_headers=None):
    if not extra_headers:
        extra_headers = {}

    if not status_code:
        status_code = 200

    # Set the application/json mimetype
    extra_headers['Content-Type'] = 'application/json'

    return (json.dumps(data), status_code, extra_headers)

