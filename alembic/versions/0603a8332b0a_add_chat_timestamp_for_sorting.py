"""Add chat timestamp for sorting

Revision ID: 0603a8332b0a
Revises: d3aab9f0dba5
Create Date: 2024-10-14 01:48:20.851012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0603a8332b0a'
down_revision: Union[str, None] = 'd3aab9f0dba5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('name', sa.String(), nullable=False))
    op.add_column('chats', sa.Column('last_message_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'last_message_at')
    op.drop_column('chats', 'name')
    # ### end Alembic commands ###
