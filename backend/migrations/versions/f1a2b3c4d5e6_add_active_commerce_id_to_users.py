"""add active_commerce_id to users

Revision ID: f1a2b3c4d5e6
Revises: 8b3c4c060ba1
Create Date: 2026-06-27

"""
from alembic import op
import sqlalchemy as sa


revision = 'f1a2b3c4d5e6'
down_revision = '8b3c4c060ba1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('active_commerce_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_users_active_commerce',
        'users', 'commerces',
        ['active_commerce_id'], ['id'],
        ondelete='SET NULL',
    )


def downgrade():
    op.drop_constraint('fk_users_active_commerce', 'users', type_='foreignkey')
    op.drop_column('users', 'active_commerce_id')
