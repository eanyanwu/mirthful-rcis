class HttpRequestException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            'error_message': self.message
        }

class BadRequest(HttpRequestException):
    def __init__(self, message):
        HttpRequestException.__init__(self, 
                                      message=message,
                                      status_code=400)

class Unauthorized(HttpRequestException):
    def __init__(self, message):
        HttpRequestException.__init__(self,
                                      message=message,
                                      status_code=401)

