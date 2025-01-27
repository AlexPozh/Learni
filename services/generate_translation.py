import logging

from db.crud.word import get_words
from db.crud.ru_word import create_multiple_ru_translation
from db.database import db_manager
from tasks.tasks import generate_translation, process_ru_words
from core.schemas.word_schema import CreateRuWordDB

logger = logging.getLogger("development")

async def process_translation():
    try:
        words = []
        ids = []
        session_gen = db_manager.session_getter()
        session = await anext(session_gen)
        limit = 75
        offset = 0
        while limit <= 6000:

            for row in await get_words(session=session, limit=limit, offset=offset): # ADD LIMIT AND OFFSET HERE. Count of words 5943
                words.append(f"{row.word}-{row.word_level}-{row.part_speech},")
                ids.append(row.id)
            
            # call a task
            result = generate_translation.delay(words)
            while not result.ready():
                pass
            
            logger.debug("The task generate_translation() succeeded")

            # call a task
            ru_words = process_ru_words.delay(result.get())
            while not ru_words.ready():
                pass
            
            ru_trans = list(ru_words.get())
            logger.debug("The task process_ru_words() succeeded")

            for i, tran in zip(ids, ru_trans):
                tran.update(eng_word_id=i)
            offset += 75
            limit += 75

            await create_multiple_ru_translation(session=session, words_scheme=[CreateRuWordDB(**item) for item in ru_trans])


    except Exception:
        logger.exception("Something went wrong")

    finally:
        await session.aclose()

