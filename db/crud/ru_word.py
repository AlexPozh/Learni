import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from core.schemas.word_schema import GetRuWordDB, CreateRuWordDB
from ..models.word import Word

logger = logging.getLogger("development")


async def create_multiple_ru_translation(
    session: AsyncSession,
    words_scheme: list[CreateRuWordDB]
) -> None:
    try:
        words = [CreateRuWordDB(**word_scheme.model_dump()) for word_scheme in words_scheme]
        session.add_all(words)
        await session.commit()
        logger.debug("Ru translatino added successfully")

    except Exception:
        logger.exception("Something went wrong")
    finally:
        await session.aclose()