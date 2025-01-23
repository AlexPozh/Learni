import asyncio
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from db.database import db_manager
from core.schemas.word_schema import CreateEngWordDB
from db.crud.word import create_multiple_words


logger = logging.getLogger("development")


class VocabularyParser:
    BASE_URL: str = "https://www.oxfordlearnersdictionaries.com/"
    WORDS_URL: str = f"{BASE_URL}wordlists/oxford3000-5000"  # 5k words
    
    UL_TAG: str = "top-g"                                    # <ul> tag which contains <li> elements
    LI_TAG: str = "li"                                       # <li> tag which contains each word
    WORD_TAG: str = "a"
    PART_SPEECH_TAG: str = "pos"                             #  class
    LEVEL_LANG_TAG: str = "belong-to"                        # class
    AUDIO_ATTRIBUTE: str = "data-src-mp3"

    COOKIE_INFO: str = "onetrust-close-btn-container"
    FILTER_BUTTON: str = "wordlistsFilters"                  # id
    OXFORD_5000_WORDS_XPATH: str = '//*[@id="filterList"]/option[1]'
    DONE_BUTTON: str = 'saveFilters'

    eng_words: list[CreateEngWordDB] = []

    def __init__(self):
        pass
    
    async def __add_to_db(self):
        session_gen = db_manager.session_getter()
        session = await anext(session_gen)
        await create_multiple_words(
                session=session,
                words_scheme=self.eng_words
            )
    
    def get_uk_audio_xpath(self, n: int = 1):
        return f'//*[@id="wordlistsContentPanel"]/ul/li[{n}]/div/div[1]'
    
    def get_us_audio_xpath(self, n: int = 1):
        return f'//*[@id="wordlistsContentPanel"]/ul/li[{n}]/div/div[2]'
    
    async def parse(self) -> list[CreateEngWordDB]:
        logger.info("Start parsing process...")
        try:
            browser = webdriver.Chrome()
            browser.get(self.WORDS_URL)
            await asyncio.sleep(2)
            
            # close the cookie acception order 
            browser.find_element(By.ID, self.COOKIE_INFO).click()
            await asyncio.sleep(2)
            
            # find "Filter" button to change count of words
            browser.find_element(By.ID, self.FILTER_BUTTON).click()
            await asyncio.sleep(2)
            
            # choose words
            browser.find_element(By.XPATH, self.OXFORD_5000_WORDS_XPATH).click()
            await asyncio.sleep(2)
            
            # accept new filter
            browser.find_element(By.ID, self.DONE_BUTTON).click()
            await asyncio.sleep(2)
            
            ul_tag = browser.find_element(By.CLASS_NAME, self.UL_TAG)
            await asyncio.sleep(1)
            logger.info("Creating CreateEngWordDB schemas...")
            li_tags = ul_tag.find_elements(By.TAG_NAME, self.LI_TAG)
            count_words = len(li_tags)
            for number, data in enumerate(li_tags, start=1):
                try:
                    if 1 <= number <= count_words:
                        self.eng_words.append(
                            CreateEngWordDB(
                                word=f"{data.find_element(By.TAG_NAME, self.WORD_TAG).text.strip()}",
                                part_speech=f"{data.find_element(By.CLASS_NAME, self.PART_SPEECH_TAG).text.strip()}",
                                word_level=f"{data.find_element(By.CLASS_NAME, self.LEVEL_LANG_TAG).text.strip()}",
                                file_uk_link=f"{data.find_element(By.XPATH, self.get_uk_audio_xpath(number)).get_attribute(self.AUDIO_ATTRIBUTE).strip()}",
                                file_us_link=f"{data.find_element(By.XPATH, self.get_us_audio_xpath(number)).get_attribute(self.AUDIO_ATTRIBUTE).strip()}"
                            )
                        )
                        logger.info("%s raw DONE", number)

                    else: 
                        continue
                except NoSuchElementException:
                    continue
        except Exception:
            logger.exception("Something went wrong")
        finally:
            browser.quit()

        logger.info("Finish parsing process...")
        logger.info("Start inserting data to db...")
        await self.__add_to_db()


    async def load_mp3(self):
        pass

parser = VocabularyParser()
