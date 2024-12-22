from fastapi import HTTPException, status


class UserUnauthorized(HTTPException):
    def __init__(self, status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid credentials", headers = None):
        super().__init__(status_code, detail, headers)
