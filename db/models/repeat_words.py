from datetime import date

from sqlalchemy import ForeignKey, func, Enum, Date, text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import Base
from ..enums.repeat_interval import RepeatIntervalEnum

class RepeatWord(Base):
    __tablename__ = "repeat_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[date] = mapped_column(nullable=False, server_default=func.now())
    next_review_at: Mapped[date] = mapped_column(Date(), nullable=False, server_default=func.now())
    interval_days: Mapped[RepeatIntervalEnum] = mapped_column(Enum(RepeatIntervalEnum), nullable=False)

    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="repeated_word", uselist=False)    # type: ignore
    word: Mapped["Word"] = relationship(back_populates="repeated_word", uselist=False)    # type: ignore
    