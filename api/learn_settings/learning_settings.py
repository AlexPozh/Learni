import logging

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.learn_settings import LearniConfigScheme, LearniConfigDB
from db.models.user import User
from db.crud.learning_config import create_learni_config
from auth.dependencies import get_user_by_token_payload
from db.database import db_manager

logger = logging.getLogger("development")


settings_router = APIRouter(
    prefix="/learni_config"
)

@settings_router.post("")
async def post_user_config(
    learni_settings: LearniConfigScheme,
    session: AsyncSession = Depends(db_manager.session_getter),
    user: User = Depends(get_user_by_token_payload)
):
    print(f"learni_settings: {learni_settings}")
    try:
        await create_learni_config(
            session=session,
            learni_config=LearniConfigDB(
                user_id=user.id,
                learning_level=learni_settings.learning_level,
                count_learn_words=learni_settings.count_learn_words,
                notification=learni_settings.notification
            )
        )
        return RedirectResponse("/home", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as error:
        logger.exception("%r", error)