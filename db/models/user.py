from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, func, LargeBinary

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    hash_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_email_confirmed: Mapped[bool] = mapped_column(nullable=True)
    registered_at: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())

    learning_config: Mapped["LearningConfig"] = relationship(back_populates="user", uselist=False)       # type: ignore
    my_words: Mapped[list["MyWords"]] = relationship(back_populates="user", uselist=True)                # type: ignore
    learnt_words: Mapped[list["LearntWord"]] = relationship(back_populates="user", uselist=True)         # type: ignore
    repeated_word: Mapped[list["RepeatWord"]] = relationship(back_populates="user", uselist=True)        # type: ignore