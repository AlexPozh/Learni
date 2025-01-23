"""changed nullable flag for word model

Revision ID: 2e0268e40dc7
Revises: 2b7ad32a2c22
Create Date: 2025-01-03 14:00:40.118446

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e0268e40dc7"
down_revision: Union[str, None] = "2b7ad32a2c22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "words",
        "translation",
        existing_type=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.alter_column(
        "words", "example_sent", existing_type=sa.TEXT(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "words", "example_sent", existing_type=sa.TEXT(), nullable=False
    )
    op.alter_column(
        "words",
        "translation",
        existing_type=sa.VARCHAR(length=100),
        nullable=False,
    )
    # ### end Alembic commands ###
