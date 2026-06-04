from rest_framework import status


class APIBaseException(Exception):
    data = None
    message = None

    def __init__(self, message, data=None, **kwargs):
        super(APIBaseException, self).__init__(message)
        self.message = message
        self.data = data

class APIException(APIBaseException):
    api_error = None
    http_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message, api_error=400, data=None, http_status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
        super(APIException, self).__init__(message, data, **kwargs)
        self.api_error = api_error
        self.http_status_code = http_status_code


class APIValidationException(APIException):
    def __init__(self, message, api_error=400, data=None, **kwargs):
        super(APIValidationException, self).__init__(message, api_error, data, status.HTTP_400_BAD_REQUEST, **kwargs)