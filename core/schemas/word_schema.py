from pydantic import BaseModel


class CreateEngWordDB(BaseModel):
    word: str
    part_speech: str
    word_level: str
    file_us_link: str
    file_uk_link: str
  