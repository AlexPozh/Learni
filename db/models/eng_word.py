from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Text, Enum, Boolean

from .base import Base
from ..enums.level_word import LevelWordEnum


class EngWord(Base):
    __tablename__ = "eng_words"

    id: Mapped[int] = mapped_column(primary_key=True)

    word: Mapped[str] = mapped_column(String(75), nullable=False)
    word_level: Mapped[LevelWordEnum] = mapped_column(Enum(LevelWordEnum), nullable=False)
    part_speech: Mapped[str] = mapped_column(String(50), nullable=False)
    file_us_link: Mapped[str] = mapped_column(String(255), nullable=False)
    file_uk_link: Mapped[str] = mapped_column(String(255), nullable=False)

    ru_learni: Mapped["Word"] = relationship(back_populates="eng_word", uselist=False)    # type: ignore