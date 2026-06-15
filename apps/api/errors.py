from enum import IntEnum


class APIError(IntEnum):
    @classmethod
    def get(cls, key: str) -> int:
        try:
            return cls[key]
        except KeyError:
            return 500


class APIErrorExtender(APIError):

    #user errors
    missing_username=10000



# class APIError(Enum):
#     @staticmethod
#     def api_error_for_http_status_code(http_status_code):
#         try:
#             return APIError(http_status_code)
#         except (BaseException, Exception):
#             return APIError.error_generic_500
#
#
# @unique
# class APIErrorGeneric(APIError):
#     # Generic default errors
#     error_generic_bad_request_400 = 400
#     error_generic_401 = 401
#     error_generic_402 = 402
#     error_generic_403 = 403
#     error_generic_404 = 404
#     error_generic_405 = 405
#     error_generic_406 = 406
#     error_generic_409 = 409
#     error_generic_410 = 410
#     error_generic_412 = 412
#     error_generic_500 = 500
#     error_generic_501 = 501