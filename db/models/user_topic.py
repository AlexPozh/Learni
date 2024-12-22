
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserTopic(Base):
    __tablename__ = "user_topic"

    id: Mapped[int] = mapped_column(primary_key=True)

    learn_config_id: Mapped[int] = mapped_column(ForeignKey("learning_config.user_id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), primary_key=True)

    