import json

def create_error_response(message, status_code, extra_headers=None):
    if not extra_headers:
        extra_headers = {}

    error = { 'error_message': message }

    # Set the application/json mimetype
    extra_headers['Content-Type'] = 'application/json'

    return (json.dumps(error), status_code, extra_headers)

def create_json_response(data, status_code, extra_headers=None):
    if not extra_headers:
        extra_headers = {}

    # Set the application/json mimetype
    extra_headers['Content-Type'] = 'application/json'

    return (json.dumps(data), status_code, extra_headers)

