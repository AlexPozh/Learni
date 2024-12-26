from datetime import date

from sqlalchemy import Date, func, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class LearntWord(Base):
    __tablename__ = "learnt_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[date] = mapped_column(nullable=False, server_default=func.now())
    next_review_at: Mapped[date] = mapped_column(Date(), nullable=False, server_default=text("NOW() + interval '10 days'"))

    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="learnt_words", uselist=False)    # type: ignore
    word: Mapped["Word"] = relationship(back_populates="learnt_words", uselist=False)    # type: ignore
    