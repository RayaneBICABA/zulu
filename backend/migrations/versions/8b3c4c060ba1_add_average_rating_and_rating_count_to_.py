"""add average_rating and rating_count to commerce_stats

Revision ID: 8b3c4c060ba1
Revises: ead9a6fc2c17
Create Date: 2026-06-27 10:47:28.919279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b3c4c060ba1'
down_revision = 'ead9a6fc2c17'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('commerce_stats', schema=None) as batch_op:
        batch_op.add_column(sa.Column('average_rating', sa.Numeric(precision=3, scale=2), nullable=True))
        batch_op.add_column(sa.Column('rating_count', sa.Integer(), nullable=True))

    op.execute("UPDATE commerce_stats SET average_rating = 0.00, rating_count = 0")

    with op.batch_alter_table('commerce_stats', schema=None) as batch_op:
        batch_op.alter_column('average_rating', nullable=False, server_default='0.00')
        batch_op.alter_column('rating_count', nullable=False, server_default='0')


def downgrade():
    with op.batch_alter_table('commerce_stats', schema=None) as batch_op:
        batch_op.drop_column('rating_count')
        batch_op.drop_column('average_rating')
