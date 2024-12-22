"""created learning_config table

Revision ID: 55a82b0b3fd0
Revises: 81e29a20531b
Create Date: 2024-12-17 17:17:52.172786

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "55a82b0b3fd0"
down_revision: Union[str, None] = "81e29a20531b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "learning_config",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("learning_level", sa.String(length=12), nullable=False),
        sa.Column("count_learn_words", sa.Integer(), nullable=False),
        sa.Column("notification", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("learning_config")
    # ### end Alembic commands ###
