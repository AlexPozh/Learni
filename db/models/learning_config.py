
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class LearningConfig(Base):
    __tablename__ = "learning_config"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    learning_level: Mapped[str] = mapped_column(String(12), nullable=False)
    count_learn_words: Mapped[int] = mapped_column(nullable=False)
    notification: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="learning_config", uselist=False)                  # type: ignore
    topic: Mapped[list["Topic"]] = relationship(back_populates="learning_config", secondary="user_topic") # type: ignore