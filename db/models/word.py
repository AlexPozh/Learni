
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Text, Enum

from .base import Base
from ..enums.level_word import LevelWordEnum

class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)

    word: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    translation: Mapped[str] = mapped_column(String(100), nullable=False)
    example_sent: Mapped[str] = mapped_column(Text(), nullable=False)
    word_level: Mapped[LevelWordEnum] = mapped_column(Enum(LevelWordEnum), nullable=False)

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))

    topic: Mapped["Topic"] = relationship(back_populates="word", uselist=False)                         # type: ignore
    learnt_words: Mapped[list["LearntWord"]] = relationship(back_populates="word", uselist=True)        # type: ignore
    repeated_word: Mapped[list["RepeatWord"]] = relationship(back_populates="word", uselist=True)        # type: ignore