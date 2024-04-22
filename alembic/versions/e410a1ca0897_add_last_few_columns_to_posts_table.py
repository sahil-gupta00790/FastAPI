"""add last few columns to posts table

Revision ID: e410a1ca0897
Revises: 7e0588eecfed
Create Date: 2024-04-22 15:22:29.205055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e410a1ca0897'
down_revision: Union[str, None] = '7e0588eecfed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False , server_default='TRUE'),)
    op.add_column('posts',sa.Column(
        'created_at' , sa.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.text('NOW()')
    ),)
    
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
