
from fastapi import APIRouter, Depends, Form

from schemas.user_schema import UserSchema
from schemas.token_schema import TokenInfo
from exceptions.auth_exception import UserUnauthorized
import auth_utils

router = APIRouter(prefix="/auth", tags=["JWT"])


def validate_auth_user(
    email: str = Form(),
    password: str = Form()
):
    pass

@router.post("/login/", response_model=TokenInfo)
def login(
    user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.email,
        "username": user.username if user.username else "no_username",
    }
    token = auth_utils.encode_jwt(
        payload=jwt_payload
    )
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )