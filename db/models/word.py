
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Text

from .base import Base
 
class Word(Base):
    __tablename__ = "ru_learn"

    id: Mapped[int] = mapped_column(primary_key=True)
    translation: Mapped[str] = mapped_column(String(100), nullable=True)
    example_sent: Mapped[str] = mapped_column(Text(), nullable=True)
   
    eng_word_id: Mapped[int] = mapped_column(ForeignKey("eng_words.id"), nullable=False)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=True)
    

    eng_word: Mapped["EngWord"] = relationship(back_populates="ru_learni", uselist=False)           # type: ignore
    topic: Mapped["Topic"] = relationship(back_populates="word", uselist=False)                          # type: ignore
    learnt_words: Mapped[list["LearntWord"]] = relationship(back_populates="word", uselist=True)         # type: ignore
    repeated_word: Mapped[list["RepeatWord"]] = relationship(back_populates="word", uselist=True)        # type: ignore 