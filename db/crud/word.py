import logging

from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.word_schema import CreateEngWordDB
from ..models.eng_word import EngWord

logger = logging.getLogger("development")


async def create_word(
    session: AsyncSession,
    word_scheme: CreateEngWordDB
) -> EngWord:
    try:
        word = EngWord(**word_scheme.model_dump())
        session.add(word)
        await session.commit()
        return word
    except Exception:
        logger.exception("Something went wrong")


async def create_multiple_words(
    session: AsyncSession,
    words_scheme: list[CreateEngWordDB]
):
    try:
        words = [EngWord(**word_scheme.model_dump()) for word_scheme in words_scheme]
        session.add_all(words)
        await session.commit()
        logger.info("Words added successfully")

    except Exception:
        logger.exception("Something went wrong")