from enum import Enum
from sqlalchemy.exc import DontWrapMixin

class DbException(Exception, DontWrapMixin):
    def __init__(self, message, error_code):
        self.error_code = error_code
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message} Error Code: {self.error_code}"

class ScrappingException(Exception):
    def __init__(self, message, error_code):
        self.error_code = error_code
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message} Error Code: {self.error_code}"


class ERROR_CODE(Enum):
    NOT_FOUND = 404
    DRIVER_ERROR = 100
