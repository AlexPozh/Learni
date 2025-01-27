from pydantic import BaseModel


class CreateEngWordDB(BaseModel):
    word: str
    part_speech: str
    word_level: str
    file_us_link: str
    file_uk_link: str
  
class GetEngWordDB(BaseModel):
    id: int
    word: str
    part_speech: str
    word_level: str


class CreateRuWordDB(BaseModel):
    translation: str | None
    example_sent: str | None
    eng_word_id: int
    topic_id: int | None = None

class GetRuWordDB(BaseModel):
    id: int
    translation: str | None
    example_sent: str | None
    topic_id: int | None
    eng_word_id: int
