
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from core.schemas.user_schema import CreateUserDB, NewPasswordDB

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

async def update_password(
    session: AsyncSession,
    update_pass: NewPasswordDB
):
    stmt = update(User).where(User.email == update_pass.email).values(hash_password=update_pass.hash_password)
    await session.execute(stmt)
    await session.commit()