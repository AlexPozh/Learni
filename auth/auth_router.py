import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from email_validator import EmailNotValidError
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse, ORJSONResponse
from redis import Redis

from core.schemas.user_schema import UserSchema, CreateUser, CreateUserDB, LoginUser, NewPasswordScheme, NewPasswordDB
from core.schemas.code_schema import EmailScheme, CodeScheme
from core.exceptions.auth_exception import UserUnauthorized, WrongVerifCode
from core.exceptions.user_exception import UserAlreadyExists
from .auth_utils import validate_password, encode_jwt, hash_password
from services.send_code import send_code, compare_codes, get_redis_conn, cache_code, is_code_exists
from db.crud.user import get_user_by_email, create_user, update_password
from db.models.user import User
from db.database import db_manager

logger = logging.getLogger("development")

auth_router = APIRouter(tags=["JWT"])

templates = Jinja2Templates(directory="templates")

# FUNCTIONS HELPERS-------------------------------------------------------------------------------
async def validate_auth_user(
    user_log: LoginUser,
    session: AsyncSession = Depends(db_manager.session_getter)
) -> User:
    try:
        if not (user := await get_user_by_email(session, user_log.email)):
            raise UserUnauthorized
    
        if validate_password(
            password=user_log.password,
            hashed_pwd=user.hash_password
        ):
            return user
        raise UserUnauthorized
    except Exception as error:
        logger.exception("%r", error)
        raise UserUnauthorized

async def is_user_exists(
    user_email: EmailScheme,
    session: AsyncSession
) -> bool:
    print(f"is_user_exists - f{user_email}")

    try:
        if not (user := await get_user_by_email(session, user_email.email)):
            raise UserUnauthorized
        else:
            return True
    except Exception as error:
        logger.exception("%r", error)
        raise UserUnauthorized


# POST requests-------------------------------------------------------------------------------
@auth_router.post("/auth/login/")
async def login(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.email,
        "username": user.username if user.username else "no_username",
    }
    token = encode_jwt(
        payload=jwt_payload
    )
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="strict",
        max_age=300
    )
    return response


@auth_router.post("/auth/register/")
async def register(
    user: CreateUser,
    session: AsyncSession = Depends(db_manager.session_getter),
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
            "username": user.username if user.username else "unknown",
        }
        token = encode_jwt(
            payload=jwt_payload
        )

        response = RedirectResponse(url="/home?new_user=true", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            samesite="strict",
            max_age=300
        )
        return response

    except IntegrityError as error:
        raise UserAlreadyExists

    except Exception as error:
        logger.exception("%r", error)


@auth_router.post("/confirm_code/")
async def post_confirm_code(
    code: CodeScheme,
    redis: Redis = Depends(get_redis_conn)
):
    try:
        if compare_codes(code.email, code.code, redis):
            token = str(uuid.uuid4())
            cache_code(code.email, token, redis)
            return RedirectResponse(url=f"/new_password/?email={code.email}", status_code=status.HTTP_303_SEE_OTHER)
        else:
            raise WrongVerifCode
    
    except WrongVerifCode:
        raise WrongVerifCode
    except Exception as error:
        logger.exception("%r", error)


@auth_router.post("/send_code/")
async def post_send_code(
    email: EmailScheme,
    # is_user_exists: bool = Depends(is_user_exists),
    redis: Redis = Depends(get_redis_conn),
    session: AsyncSession = Depends(db_manager.session_getter)
):
    try:
        logger.debug("Inside /send_code/")
        if await is_user_exists(email, session):
            send_code(email.email, redis)
            return ORJSONResponse(content={"message": f"Code was sent successfully to {email.email}."}, status_code=200)
    
    except EmailNotValidError:
        raise UserUnauthorized
    except UserUnauthorized:
        raise UserUnauthorized
    except Exception as error:
        logger.exception("%r", error)
  

@auth_router.post("/set_new_password/")
async def post_new_password(
    data: NewPasswordScheme,
    session: AsyncSession = Depends(db_manager.session_getter)
):
    try:
        new_hashed_password = hash_password(data.password)
        await update_password(session, NewPasswordDB(
                                                    email=data.email, 
                                                    hash_password=new_hashed_password))
        
        return ORJSONResponse(content={"message": "Password changed"}, status_code=200)
    except Exception as error:
        logger.exception("%r", error)

# GET requests-------------------------------------------------------------------------------
@auth_router.get("/new_password/")
async def get_new_password(
    email: str,
    request: Request,
    redis: Redis = Depends(get_redis_conn)
):
    code = is_code_exists(email, redis)
    if code is None:
        return RedirectResponse("/login")
    
    return templates.TemplateResponse(
        "new_password.html",
        {
            "request": request
        }
    )


@auth_router.get("/forgot_password/")
async def get_forgot_pwd(
    request: Request,
):
    return templates.TemplateResponse(
        "forgot_pwd.html",
        {
            "request": request
        }
    )

@auth_router.get("/login/")
async def get_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@auth_router.get("/register/")
async def get_register(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request
        }
    )