
from fastapi import APIRouter, Depends

from core.schemas.user_schema import UserSchema
from db.models.user import User
from auth.dependencies import get_user_by_token_payload

user_profile = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


async def get_current_auth_user(
    user: User | dict = Depends(get_user_by_token_payload)
) -> UserSchema:
    if isinstance(user, dict):
        raise user["error"]
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
