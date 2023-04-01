"""products

Revision ID: 2186e82da80c
Revises: 
Create Date: 2023-03-31 22:26:25.586751

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '2186e82da80c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
  products = op.create_table('products',
                             sa.Column('id', sa.Integer(), nullable=False),
                             sa.Column('name', sa.String(255), nullable=False),
                             sa.Column('description', sa.Text(),
                                       nullable=False),
                             sa.Column('price', sa.Float(
                               10, 2), nullable=False),
                             sa.PrimaryKeyConstraint('id'))
  pass


def downgrade() -> None:
  op.drop_table('products')
  pass
