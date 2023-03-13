"""merging 2 heads

Revision ID: 5d9c2fd9fd4f
Revises: 83c74f9324d5, cb0d39b38df7
Create Date: 2023-03-13 02:34:44.633880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d9c2fd9fd4f'
down_revision = ('83c74f9324d5', 'cb0d39b38df7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
