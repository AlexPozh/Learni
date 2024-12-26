
from jwt import InvalidTokenError
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.user_schema import UserSchema
from core.exceptions.user_exception import UserNotFound, InvalidToken
from auth.auth_utils import decode_jwt
from db.database import db_manager
from db.crud.user import get_user_by_email
from db.models.user import User

user_profile = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/"
)

async def get_user_by_token_payload(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_manager.session_getter)
) -> User:
    try:
        payload = decode_jwt(
            jwt_token=token
        )
    except InvalidTokenError:
        raise InvalidToken
    if not (user := await get_user_by_email(
        session=session,
        email=payload["sub"]
    )):
        raise UserNotFound
    return user


async def get_current_auth_user(
    user: User = Depends(get_user_by_token_payload)
) -> UserSchema:
    return UserSchema(
        username=user.username,
        email=user.email,
        is_email_confirmed=user.is_email_confirmed,
        registered_at=user.registered_at
    )


@user_profile.get("/me/")
async def get_my_profile_info(
    user: UserSchema = Depends(get_current_auth_user)
) -> UserSchema:
    return user
