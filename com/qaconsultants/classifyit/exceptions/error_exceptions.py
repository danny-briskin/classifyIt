class AbstractException(Exception):
    status_code = 400
    message_key = 'error'

    def __init__(self, message, status_code=None, message_key=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if message_key is not None:
            self.message_key = message_key
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv[self.message_key] = self.message
        return rv


class InvalidParameter(AbstractException):
    """
    Raises when request parameter is invalid
    """
    message_key = 'invalid parameter'


class MissingParameter(AbstractException):
    status_code = 422
    message_key = 'missing parameter'


class MethodUnsupported(AbstractException):
    status_code = 405
    message_key = 'unsupported method'


class ImageException(AbstractException):
    status_code = 500
    message_key = 'image processing error'
