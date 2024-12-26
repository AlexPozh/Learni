
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from core.schemas.user_schema import CreateUserDB

async def get_user_by_email(
    session: AsyncSession,
    email: str
) -> User:
    stmt = select(User).where(User.email == email)
    result = await session.scalar(stmt)
    return result


async def create_user(
    session: AsyncSession,
    user_create: CreateUserDB
):
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user