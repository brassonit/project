"""add show is_active column

Revision ID: 704e10e80afc
Revises: 8e06107e4fde
Create Date: 2026-11-25 23:40:24.743196
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '704e10e80afc'
down_revision: Union[str, None] = '8e06107e4fde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "shows",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        schema="com",
    )


def downgrade() -> None:
    op.drop_column("shows", "is_active", schema="com")
