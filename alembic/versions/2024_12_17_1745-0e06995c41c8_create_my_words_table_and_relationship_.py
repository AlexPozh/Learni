"""create my_words table and relationship with user

Revision ID: 0e06995c41c8
Revises: 55a5745c04ed
Create Date: 2024-12-17 17:45:55.296734

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e06995c41c8"
down_revision: Union[str, None] = "55a5745c04ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "my_words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("word", sa.String(length=55), nullable=False),
        sa.Column("translation", sa.String(length=255), nullable=False),
        sa.Column("example_sent", sa.Text(), nullable=True),
        sa.Column(
            "added_at",
            sa.Date(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("word"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("my_words")
    # ### end Alembic commands ###