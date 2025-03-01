import logging

from jwt import InvalidTokenError
from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions.user_exception import UserNotFound, InvalidToken
from auth.auth_utils import decode_jwt
from db.database import db_manager
from db.crud.user import get_user_by_email
from db.models.user import User

logger = logging.getLogger("development")


async def get_user_by_token_payload(
    request: Request,
    session: AsyncSession = Depends(db_manager.session_getter)
) -> User | dict[str, InvalidToken | UserNotFound]:    
    try:
        token = request.cookies.get("access_token")
        payload = decode_jwt(
            jwt_token=token
        )

    except InvalidTokenError:
        logger.debug("%s", {"error": InvalidToken()})
        return {
            "error": InvalidToken()
        }
    if not (user := await get_user_by_email(
        session=session,
        email=payload["sub"]
    )):
        logger.debug("%s", {"error": UserNotFound()})
        return {
            "error": UserNotFound()
        }
    return user


async def permit_access(
    user: User | dict = Depends(get_user_by_token_payload)
) -> User | RedirectResponse:
    if isinstance(user, User):
        return User
    redirect = RedirectResponse(url="/login/")
    return redirect