from pydantic import BaseModel



class LearniConfigScheme(BaseModel):
    learning_level: str
    count_learn_words: int
    notification: bool 

class LearniConfigDB(BaseModel):
    user_id: int
    learning_level: str
    count_learn_words: int
    notification: bool 