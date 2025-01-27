from contextlib import asynccontextmanager
import logging
import logging.config
import asyncio

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
import yaml

from db.database import db_manager
from auth.auth_router import auth_router
from api.profile.user_profile import user_profile
from core.config import settings
from services.parsing import parser
from services.load_pronounce import load_pron
from services.generate_translation import process_translation

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

# including routers here
main_app.include_router(auth_router)
main_app.include_router(user_profile)

@main_app.get("/", tags=["Greeting"], description="This endpoint sends just 'Hello!'")
def hello():
    return {
        "message": "Hello!"
    }

# Only for parsing words / pronounce
async def main():
    # await load_pron.get_url_links()
    # await load_pron.load_pronounce_files()
    await process_translation()
    
if __name__ == "__main__":
    # uvicorn.run(
    #     "main:main_app",
    #     host=settings.api.host,
    #     port=int(settings.api.port),
    #     reload=True,
    # )

    # Only for parsing
    asyncio.run(main())