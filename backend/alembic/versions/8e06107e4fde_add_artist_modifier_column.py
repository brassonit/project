"""add artist modifier column

Revision ID: 8e06107e4fde
Revises: d06a2b3ca813
Create Date: 2026-11-19 21:50:44.921634
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e06107e4fde'
down_revision: Union[str, None] = 'd06a2b3ca813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "artists",
        sa.Column("modifier", sa.Text(), nullable=False, server_default=""),
        schema="com",
    )


def downgrade() -> None:
    op.drop_column("artists", "modifier", schema="com")
