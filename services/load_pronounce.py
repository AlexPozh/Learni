import logging
import time

import requests

from db.database import db_manager
from db.crud.word import get_words

logger = logging.getLogger("development")

class LoadPronounce:
    BASE_URL: str = "https://www.oxfordlearnersdictionaries.com"

    PRON_LINKS: list[tuple[str, str]] = []
    
    SAVE_US_PATH: str = "/home/alex/Рабочий стол/Learni_app/Learni/pron_files/us/" # {self.SAVE_US_PATH}{us_link.split("/")[-1]}
    SAVE_UK_PATH: str = "/home/alex/Рабочий стол/Learni_app/Learni/pron_files/uk/" # {self.SAVE_UK_PATH}{uk_link.split("/")[-1]}

    def __init__(self):
        pass

    async def get_url_links(self) -> list[tuple[str, str]]:
        session_gen = db_manager.session_getter()
        session = await anext(session_gen)
        for row in await get_words(session=session):    # ADD A LIMIT HERE
            prons = row.file_us_link, row.file_uk_link
            self.PRON_LINKS.append(prons)
        return self.PRON_LINKS
    

    def install_file(self, url: str, save_path: str = ""):
        headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.oxfordlearnersdictionaries.com/"
            }
        response = requests.get(f"{self.BASE_URL}{url}", headers=headers)
        if response.status_code == 200:
            with open(f"{save_path}{url.split("/")[-1]}", "wb") as f:
                f.write(response.content)
            logger.debug("File [%s] was installed", url.split("/")[-1])
        else:
            logger.error("Status code: %s", response.status_code) 


    async def load_pronounce_files(self) -> None:
        logger.info("Start loadind media files process...")
        try:
    
            for us_link, uk_link in self.PRON_LINKS:
                self.install_file(us_link, self.SAVE_US_PATH)
                time.sleep(0.2)
                self.install_file(uk_link, self.SAVE_UK_PATH)

            logger.info("Finished loading media process")
        except Exception:
            logger.exception("Something went wrong")

load_pron = LoadPronounce()