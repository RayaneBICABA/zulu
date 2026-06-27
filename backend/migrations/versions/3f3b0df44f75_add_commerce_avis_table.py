"""add commerce avis table

Revision ID: 3f3b0df44f75
Revises: 97545edcb905
Create Date: 2026-06-27 13:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f3b0df44f75'
down_revision = '97545edcb905'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('commerce_avis',
    sa.Column('commerce_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Integer(), nullable=False),
    sa.Column('commentaire', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['commerce_id'], ['commerces.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'commerce_id', name='uq_avis_user_commerce')
    )
    op.create_index(op.f('ix_commerce_avis_commerce_id'), 'commerce_avis', ['commerce_id'], unique=False)
    op.create_index(op.f('ix_commerce_avis_user_id'), 'commerce_avis', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_commerce_avis_user_id'), table_name='commerce_avis')
    op.drop_index(op.f('ix_commerce_avis_commerce_id'), table_name='commerce_avis')
    op.drop_table('commerce_avis')
