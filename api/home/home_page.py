
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from auth.dependencies import permit_access
from db.models.user import User

home_router = APIRouter(
    prefix="/home",
    tags=["Home"]
)

templates = Jinja2Templates(directory="templates")

@home_router.get("")
async def get_home_page(
    request: Request,
    # user_or_redirect: User | RedirectResponse = Depends(permit_access),
    new_user: str | None = None,
):
    # if isinstance(user_or_redirect, RedirectResponse):
    #     return user_or_redirect
    
    if new_user is None:
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request
            }
        )

    return templates.TemplateResponse(
        "greeting.html",
        {
            "request": request
        }
    )


