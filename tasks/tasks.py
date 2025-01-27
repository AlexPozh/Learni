
from g4f.client import Client

from .celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def generate_translation(self, eng_words: list[str]) -> str:
    try:
        prompt = f""" 
    Chat, translate (write one form, also if word has many translations - take 2-3. Dont explain the word, just write a form) these words to russian {eng_words} and make 2 example sentences for their english level with this word and double it with russian translation below. Write the answer by this pattern (notice, that the symbols /// needs to separate translations, so write this /// in the begining and in the end):
    ///
    English_word: english_word_1
    Translation: translation_1, translation_2 (if it exists)
    Example sentences: example_sentence_1. example_sentence_2
    ///
    English_word: english_word_2
    Translation: translation_1, translation_2 (if it exists)
    Example sentences: example_sentence_1. example_sentence_2
    ///
    English_word: english_word_3
    Translation: translation_1, translation_2 (if it exists)
    Example sentences: example_sentence_1. example_sentence_2
    ///
    ...
    ///
    """
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            web_search=False
        )
        return response.choices[0].message.content
    except Exception as error:
        raise self.retry(exc=error, countdown=3)

@celery_app.task()
def process_ru_words(words: str) -> list[dict]:
    result = []
    trans = words.strip().split("///")
    for i in range(len(trans)):
        if len(trans[i]) != 0:
            one_tran = trans[i].strip().split("\n")
            try:
                result.append(
                {
                    "translation": one_tran[1].split(":")[1].strip(),
                    "example_sent": one_tran[2].split(":")[1].strip()
                }
                )
            except IndexError:
                pass
        else:
            pass
    return result

