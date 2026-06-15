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
    missing_email=10001