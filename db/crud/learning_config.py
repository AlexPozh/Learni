

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.learning_config import LearningConfig
from core.schemas.learn_settings import LearniConfigDB



async def create_learni_config(
    session: AsyncSession,
    learni_config: LearniConfigDB
):
    conf = LearningConfig(**learni_config.model_dump())
    session.add(conf)
    await session.commit()
