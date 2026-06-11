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

def custom_exception_handler(exc, context):

    # Eccezioni rest_framework 
    response = exception_handler(exc, context)

    # =========================
    # ECCEZIONI CUSTOM
    # =========================
    if isinstance(exc, APIBaseException):
        return Response(
            {
                "message": exc.message,
                "api_error": getattr(exc, "api_error", exc.__class__.__name__),
                "data": exc.data,
                "http_status_code": exc.http_status_code,
            },
            status=exc.http_status_code,
        )

    # =========================
    # ERRORI DRF
    # =========================
    if response is not None:
        return Response(
            {
                "message": "Internal DRF server error",
                "api_error": exc.__class__.__name__,
                "data": response.data,
                "http_status_code": response.status_code,
            },
            status=response.status_code,
        )

    # =========================
    # ERRORI DJANGO / PYTHON GENERICI
    # =========================
    return Response(
        {
            "message": str(exc) if settings.DEBUG else "Internal server error",
            "api_error": exc.__class__.__name__,
            "data": None,
            "http_status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
# PRODUCTION best practice
# str(exc) if settings.DEBUG else "Internal server error"