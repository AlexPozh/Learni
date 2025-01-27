import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from core.schemas.word_schema import CreateEngWordDB, GetEngWordDB
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
        logger.info("Word added successfully")
        return word
    except Exception:
        logger.exception("Something went wrong")
    finally:
        await session.aclose()


async def create_multiple_words(
    session: AsyncSession,
    words_scheme: list[CreateEngWordDB]
):
    try:
        words = [EngWord(**word_scheme.model_dump()) for word_scheme in words_scheme]
        session.add_all(words)
        await session.commit()
        logger.debug("Word added successfully")

    except Exception:
        logger.exception("Something went wrong")
    finally:
        await session.aclose()


async def get_words_filter(
    session: AsyncSession,
    id: int | None = None,
    word: str | None = None, 
    word_level: str | None = None,
    part_speech: str | None = None,
    limit: int = 10
) -> list[GetEngWordDB]:
    filter_raw = id, word, word_level, part_speech
    try:
        match filter_raw:
            case int(id), _, _, _:
                stmt = select(EngWord.id, EngWord.word, EngWord.word_level, EngWord.part_speech).where(EngWord.id == id)
            
            case _, str(word), _, _:
                stmt = select(EngWord.id, EngWord.word, EngWord.word_level, EngWord.part_speech).where(EngWord.word == word).limit(limit)
            
            case _, _, str(word_level), str(part_speech):
                stmt = select(EngWord.id, EngWord.word, EngWord.word_level, EngWord.part_speech).where(
                    and_(
                        EngWord.word_level == word_level,
                        EngWord.part_speech == part_speech
                        )
                    ).limit(limit)
            
            case _, _, str(word_level), _:
                stmt = select(EngWord.id, EngWord.word, EngWord.word_level, EngWord.part_speech).where(EngWord.word_level == word_level).limit(limit)
            
            case _, _, _, str(part_speech):
                stmt = select(EngWord.id, EngWord.word, EngWord.word_level, EngWord.part_speech).where(EngWord.part_speech == part_speech).limit(limit)
            
            case _:
                stmt = select(EngWord).limit(limit)

        result = await session.execute(stmt)
        rows = result.all()
        return [GetEngWordDB(id=row[0], word=row[1], word_level=row[2], part_speech=row[3]) for row in rows]

    except Exception:
        logger.exception("Something went wrong")
    
    finally:
        await session.aclose()


async def get_words(
    session: AsyncSession,
    limit: int = 10,
    offset: int = 0
) -> list[GetEngWordDB]:
    try:
        stmt = select(EngWord).limit(limit).offset(offset=offset)
        result = await session.execute(stmt)
        return result.scalars().all()

    except Exception:
        logger.exception("Something went wrong")

    finally:
        await session.aclose()