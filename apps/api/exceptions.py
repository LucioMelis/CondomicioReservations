from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class APIBaseException(Exception):
    data = None
    message = None

    def __init__(self, message, data=None, **kwargs):
        super(APIBaseException, self).__init__(message)
        self.message = message
        self.data = data

class APICustomException(APIBaseException):
    api_error = None
    http_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message, api_error=400, data=None, http_status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
        super(APICustomException, self).__init__(message, data, **kwargs)
        self.api_error = api_error
        self.http_status_code = http_status_code


class APIValidationException(APICustomException):
    def __init__(self, message, api_error=400, data=None, **kwargs):
        super(APIValidationException, self).__init__(message, api_error, data, status.HTTP_400_BAD_REQUEST, **kwargs)

def _get_response(exc, response=None):

   #gestire status code
   #gestire exc message

    return Response(
        {
            "message": str(exc) if str(exc) else "Internal server error",
            "api_error": getattr(exc, "api_error", exc.__class__.__name__),
            "data": response.data if response else exc.data,
            "http_status_code": response.status_code if response else exc.http_status_code,
        },
        status=response.status_code if response else exc.http_status_code,
    )


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if isinstance(exc, APIBaseException):
        print("-------------------------EXC CUSTOM--------------------------")
        return _get_response(exc)

    if response is not None:
        print("-------------------------EXC DRF--------------------------")
        return _get_response(exc, response)

    print("-------------------------EXC DJ--------------------------")
    return _get_response(exc)

# str(exc) if settings.DEBUG else "Internal server error"