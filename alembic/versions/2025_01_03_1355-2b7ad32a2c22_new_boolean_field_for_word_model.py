"""new boolean field for word model

Revision ID: 2b7ad32a2c22
Revises: 8b1018765e52
Create Date: 2025-01-03 13:55:27.974906

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b7ad32a2c22"
down_revision: Union[str, None] = "8b1018765e52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "words", sa.Column("processed_word", sa.Boolean(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("words", "processed_word")
    # ### end Alembic commands ###
