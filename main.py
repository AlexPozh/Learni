from contextlib import asynccontextmanager
import logging
import logging.config
import time

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
import uvicorn
import yaml

from db.database import db_manager
from auth.auth_router import auth_router
from api.profile.user_profile import user_profile
from api.home.home_page import home_router
from api.root.root_page import root_router
from api.learn_settings.learning_settings import settings_router
from core.config import settings


with open(settings.log.path, settings.log.mode, encoding=settings.log.encoding) as file:
    config = yaml.safe_load(file.read())

logging.config.dictConfig(
    config=config
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shotdown
    await db_manager.engine_dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

@main_app.get("/test/")
def test(
    new_user: str | None = None
):
    return {
        "message": f"Parameter value: {new_user}. Type: {type(new_user)}"
    }

# including routers here
main_app.include_router(auth_router)
main_app.include_router(user_profile)
main_app.include_router(home_router)
main_app.include_router(root_router)
main_app.include_router(settings_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.api.host,
        port=int(settings.api.port),
        reload=True,
    )
    
    # Only for parsing words / pronounce

    # from services.parsing import parser
    # from services.load_pronounce import load_pron
    # from services.generate_translation import process_translation
    # import asyncio
    
    # async def main():
        # await load_pron.get_url_links()
        # await load_pron.load_pronounce_files()
        # await process_translation()
    
    # asyncio.run(main())