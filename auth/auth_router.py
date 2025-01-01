import logging

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.user_schema import UserSchema, CreateUser, CreateUserDB
from core.schemas.token_schema import TokenInfo
from core.exceptions.auth_exception import UserUnauthorized
from .auth_utils import validate_password, encode_jwt, hash_password
from db.crud.user import get_user_by_email, create_user
from db.models.user import User
from db.database import db_manager

logger = logging.getLogger("development")

auth_router = APIRouter(prefix="/auth", tags=["JWT"])


async def validate_auth_user(
    session: AsyncSession = Depends(db_manager.session_getter),
    username: str = Form(),
    password: str = Form()
) -> User:
    if not (user := await get_user_by_email(session, username)):
        raise UserUnauthorized
    
    if validate_password(
        password=password,
        hashed_pwd=user.hash_password
    ):
        return user
    raise UserUnauthorized


@auth_router.post("/login/", response_model=TokenInfo)
async def login(
    user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.email,
        "username": user.username if user.username else "no_username",
    }
    token = encode_jwt(
        payload=jwt_payload
    )
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


@auth_router.post("/register/", response_model=TokenInfo)
async def register(
    user: CreateUser,
    session: AsyncSession = Depends(db_manager.session_getter)
):
    hashed_pwd = hash_password(user.hash_password)
    try:
        user = await create_user(
            session=session,
            user_create=CreateUserDB(
                username=user.username,
                email=user.email,
                hash_password=hashed_pwd
            )
        )
        jwt_payload = {
            "sub": user.email,
            "username": user.username if user.username else "no_username",
        }
        token = encode_jwt(
            payload=jwt_payload
        )
        return TokenInfo(
            access_token=token,
            token_type="Bearer"
        )

    except Exception as error:
        logger.exception("%r", error)
