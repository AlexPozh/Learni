from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #shotdown
    await db_manager.engine_dispose()



main_app = FastAPI(
    lifespan=lifespan
)

@main_app.get("/")
def hello():
    return {
        "message": "Hello!"
    }