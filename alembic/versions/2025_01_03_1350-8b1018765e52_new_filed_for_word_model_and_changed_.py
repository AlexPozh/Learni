"""new filed for word model and changed word field

Revision ID: 8b1018765e52
Revises: f309499e09f6
Create Date: 2025-01-03 13:50:31.295722

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b1018765e52"
down_revision: Union[str, None] = "f309499e09f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "words", sa.Column("part_speech", sa.String(length=50), nullable=False)
    )
    op.drop_constraint("uq_words_word", "words", type_="unique")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("uq_words_word", "words", ["word"])
    op.drop_column("words", "part_speech")
    # ### end Alembic commands ###
