"""Create guides tables

Revision ID: 0001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create guide table
    op.create_table('guide',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_guide_key'), 'guide', ['key'], unique=True)
    
    # Create guide_step table
    op.create_table('guidestep',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('guide_id', sa.Integer(), nullable=False),
        sa.Column('section_index', sa.Integer(), nullable=True),
        sa.Column('step_index', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('text', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['guide_id'], ['guide.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_guidestep_guide_id'), 'guidestep', ['guide_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_guidestep_guide_id'), table_name='guidestep')
    op.drop_table('guidestep')
    op.drop_index(op.f('ix_guide_key'), table_name='guide')
    op.drop_table('guide')
