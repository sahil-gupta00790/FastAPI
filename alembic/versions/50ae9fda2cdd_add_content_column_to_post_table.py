"""add content column to post table

Revision ID: 50ae9fda2cdd
Revises: c270e4ac1f77
Create Date: 2024-04-22 14:54:26.849110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50ae9fda2cdd'
down_revision: Union[str, None] = 'c270e4ac1f77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
