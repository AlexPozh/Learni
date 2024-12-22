
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_topic: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)

    word: Mapped["Word"] = relationship(back_populates="topic", uselist=False)                                      # type: ignore
    learning_config: Mapped[list["LearningConfig"]] = relationship(back_populates="topic", secondary="user_topic")  # type: ignore