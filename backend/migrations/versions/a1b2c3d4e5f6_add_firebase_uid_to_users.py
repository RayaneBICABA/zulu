"""add firebase_uid to users

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2026-06-30

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = 'f1a2b3c4d5e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('firebase_uid', sa.String(length=255), nullable=True))
    op.create_unique_constraint('uq_users_firebase_uid', 'users', ['firebase_uid'])
    op.create_index('ix_users_firebase_uid', 'users', ['firebase_uid'])
    op.alter_column('users', 'password_hash', nullable=True)


def downgrade():
    op.alter_column('users', 'password_hash', nullable=False)
    op.drop_index('ix_users_firebase_uid', table_name='users')
    op.drop_constraint('uq_users_firebase_uid', 'users', type_='unique')
    op.drop_column('users', 'firebase_uid')