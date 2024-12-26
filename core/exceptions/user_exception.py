from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, status_code = status.HTTP_401_UNAUTHORIZED, detail = "User not found, try to register", headers = None):
        super().__init__(status_code, detail, headers)

class InvalidToken(HTTPException):
    def __init__(self, status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid token value", headers = None):
        super().__init__(status_code, detail, headers)