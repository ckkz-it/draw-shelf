class BaseAppException(Exception):
    message = 'Error occurred'

    def __init__(self, message=None, errors=None):
        super().__init__(message or self.message, errors)

    def __str__(self):
        return self.message


class AuthenticationFailed(BaseAppException):
    message = 'Authentication failed'
