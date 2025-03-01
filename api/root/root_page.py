from fastapi import APIRouter
from fastapi import HTTPException
from starlette.requests import Request
from fastapi import Depends
from fastapi.responses import RedirectResponse

from core.exceptions.user_exception import UserNotFound, InvalidToken
from auth.dependencies import get_user_by_token_payload
from db.models.user import User

root_router = APIRouter()


@root_router.get("/")
async def get_home_page(user: User | dict = Depends(get_user_by_token_payload)):
    if isinstance(user, User):
        return RedirectResponse(url="/home")
    return RedirectResponse(url="/login")