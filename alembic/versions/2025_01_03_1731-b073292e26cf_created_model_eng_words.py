"""created model eng_words

Revision ID: b073292e26cf
Revises: 2e0268e40dc7
Create Date: 2025-01-03 17:31:41.185488

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b073292e26cf"
down_revision: Union[str, None] = "2e0268e40dc7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ru_learn",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("translation", sa.String(length=100), nullable=True),
        sa.Column("example_sent", sa.Text(), nullable=True),
        sa.Column("topic_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topics.id"],
            name=op.f("fk_ru_learn_topic_id_topics"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ru_learn")),
    )


    op.create_foreign_key(
        op.f("fk_learnt_words_word_id_ru_learn"),
        "learnt_words",
        "ru_learn",
        ["word_id"],
        ["id"],
    )
  
    op.create_foreign_key(
        op.f("fk_repeat_words_word_id_ru_learn"),
        "repeat_words",
        "ru_learn",
        ["word_id"],
        ["id"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_repeat_words_word_id_ru_learn"),
        "repeat_words",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "repeat_words_word_id_fkey",
        "repeat_words",
        "words",
        ["word_id"],
        ["id"],
    )
    op.drop_constraint(
        op.f("fk_learnt_words_word_id_ru_learn"),
        "learnt_words",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "learnt_words_word_id_fkey",
        "learnt_words",
        "words",
        ["word_id"],
        ["id"],
    )
    op.create_table(
        "words",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "word", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
        sa.Column(
            "translation",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "example_sent", sa.TEXT(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "word_level",
            postgresql.ENUM(
                "BEGINNER", "INTERMEDIATE", "ADVANCED", name="levelwordenum"
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "topic_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "file_us_link",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "file_uk_link",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "part_speech",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "processed_word", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["topic_id"], ["topics.id"], name="words_topic_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="words_pkey"),
    )
    op.drop_table("ru_learn")
    # ### end Alembic commands ###
