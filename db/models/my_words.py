from datetime import date

from sqlalchemy import ForeignKey, String, Text, Date, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class MyWords(Base):
    __tablename__ = "my_words"

    id: Mapped[int] = mapped_column(primary_key=True)

    word: Mapped[str] = mapped_column(String(55), unique=True, nullable=False)
    translation: Mapped[str] = mapped_column(String(255), nullable=False)
    example_sent: Mapped[str] = mapped_column(Text(), nullable=True)
    added_at: Mapped[date] = mapped_column(Date(), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="my_words", uselist=False) # type: ignore