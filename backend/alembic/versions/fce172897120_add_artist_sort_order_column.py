"""add artist sort_order column

Revision ID: fce172897120
Revises: 704e10e80afc
Create Date: 2026-11-26 00:00:58.329794
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fce172897120'
down_revision: Union[str, None] = '704e10e80afc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "artists",
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        schema="com",
    )


def downgrade() -> None:
    op.drop_column("artists", "sort_order", schema="com")
