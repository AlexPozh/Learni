from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from db.database import db_manager
from auth.auth_router import auth_router
from api.profile.user_profile import user_profile
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shotdown
    await db_manager.engine_dispose()


main_app = FastAPI(
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


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.api.host,
        port=int(settings.api.port),
        reload=True,
    )