"""Initial schema

Revision ID: ef24d0ee3322
Revises:
Create Date: 2026-01-29 07:04:03.202893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ef24d0ee3322'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('role', sa.String(50), default='scientist', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Compounds table
    op.create_table(
        'compounds',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('external_id', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), index=True, nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Experiments table
    op.create_table(
        'experiments',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), index=True, nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Plates table
    op.create_table(
        'plates',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), index=True, nullable=False),
        sa.Column('barcode', sa.String(100), index=True, nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('experiment_id', sa.String(36), sa.ForeignKey('experiments.id'), nullable=False),
        sa.Column('rows', sa.Integer(), default=16, nullable=False),
        sa.Column('columns', sa.Integer(), default=24, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Wells table
    op.create_table(
        'wells',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('plate_id', sa.String(36), sa.ForeignKey('plates.id'), nullable=False),
        sa.Column('row', sa.Integer(), nullable=False),
        sa.Column('column', sa.Integer(), nullable=False),
        sa.Column('compound_id', sa.String(36), sa.ForeignKey('compounds.id'), nullable=True),
        sa.Column('concentration', sa.Float(), nullable=True),
        sa.Column('concentration_unit', sa.String(20), default='uM', nullable=False),
        sa.Column('well_type', sa.String(50), default='sample', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_wells_plate_position', 'wells', ['plate_id', 'row', 'column'], unique=True)

    # Images table
    op.create_table(
        'images',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('well_id', sa.String(36), sa.ForeignKey('wells.id'), nullable=False),
        sa.Column('s3_key', sa.String(500), nullable=False),
        sa.Column('thumbnail_s3_key', sa.String(500), nullable=True),
        sa.Column('field_index', sa.Integer(), default=0, nullable=False),
        sa.Column('channel', sa.String(50), nullable=False),
        sa.Column('channel_index', sa.Integer(), default=0, nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('pixel_size_um', sa.Float(), nullable=True),
        sa.Column('original_filename', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Well analyses table
    op.create_table(
        'well_analyses',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('well_id', sa.String(36), sa.ForeignKey('wells.id'), unique=True, nullable=False),
        sa.Column('cell_count', sa.Integer(), nullable=True),
        sa.Column('viability', sa.Float(), nullable=True),
        sa.Column('z_score', sa.Float(), nullable=True),
        sa.Column('metrics', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Dose response curves table
    op.create_table(
        'dose_response_curves',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('experiment_id', sa.String(36), sa.ForeignKey('experiments.id'), nullable=False),
        sa.Column('compound_id', sa.String(36), sa.ForeignKey('compounds.id'), nullable=False),
        sa.Column('ic50', sa.Float(), nullable=True),
        sa.Column('ec50', sa.Float(), nullable=True),
        sa.Column('hill_slope', sa.Float(), nullable=True),
        sa.Column('top', sa.Float(), nullable=True),
        sa.Column('bottom', sa.Float(), nullable=True),
        sa.Column('r_squared', sa.Float(), nullable=True),
        sa.Column('data_points', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        'ix_drc_experiment_compound',
        'dose_response_curves',
        ['experiment_id', 'compound_id'],
        unique=True
    )


def downgrade() -> None:
    op.drop_table('dose_response_curves')
    op.drop_table('well_analyses')
    op.drop_table('images')
    op.drop_index('ix_wells_plate_position', table_name='wells')
    op.drop_table('wells')
    op.drop_table('plates')
    op.drop_table('experiments')
    op.drop_table('projects')
    op.drop_table('compounds')
    op.drop_table('users')
