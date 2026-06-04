class APIBaseException(Exception):
    data = None
    message = None

    def __init__(self, message, data=None, **kwargs):
        super(APIBaseException, self).__init__(message)
        self.message = message
        self.data = data
        