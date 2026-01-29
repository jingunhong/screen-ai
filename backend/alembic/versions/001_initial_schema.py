"""initial_schema

Revision ID: 001
Revises:
Create Date: 2026-01-29

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # Compounds table
    op.create_table(
        "compounds",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("identifier", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_compounds_identifier", "compounds", ["identifier"], unique=True)

    # Projects table
    op.create_table(
        "projects",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
    )
    op.create_index("ix_projects_name", "projects", ["name"])

    # Experiments table
    op.create_table(
        "experiments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("experiment_date", sa.Date(), nullable=True),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
    )
    op.create_index("ix_experiments_name", "experiments", ["name"])

    # Plates table
    op.create_table(
        "plates",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("barcode", sa.String(100), nullable=True),
        sa.Column("format", sa.Integer(), nullable=False, server_default="384"),
        sa.Column("rows", sa.Integer(), nullable=False, server_default="16"),
        sa.Column("columns", sa.Integer(), nullable=False, server_default="24"),
        sa.Column("experiment_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["experiment_id"], ["experiments.id"]),
    )
    op.create_index("ix_plates_name", "plates", ["name"])
    op.create_index("ix_plates_barcode", "plates", ["barcode"], unique=True)

    # Wells table
    op.create_table(
        "wells",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("row", sa.Integer(), nullable=False),
        sa.Column("column", sa.Integer(), nullable=False),
        sa.Column("row_label", sa.String(2), nullable=False),
        sa.Column("column_label", sa.String(3), nullable=False),
        sa.Column("well_type", sa.String(50), nullable=False, server_default="sample"),
        sa.Column("concentration", sa.Float(), nullable=True),
        sa.Column("plate_id", sa.UUID(), nullable=False),
        sa.Column("compound_id", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["plate_id"], ["plates.id"]),
        sa.ForeignKeyConstraint(["compound_id"], ["compounds.id"]),
    )

    # Images table
    op.create_table(
        "images",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("s3_key", sa.String(1000), nullable=False),
        sa.Column("thumbnail_s3_key", sa.String(1000), nullable=True),
        sa.Column("channel", sa.String(50), nullable=False),
        sa.Column("channel_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("field_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("well_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["well_id"], ["wells.id"]),
    )

    # Analyses table
    op.create_table(
        "analyses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("analysis_type", sa.String(100), nullable=False),
        sa.Column("cell_count", sa.Integer(), nullable=True),
        sa.Column("mean_intensity", sa.Float(), nullable=True),
        sa.Column("median_intensity", sa.Float(), nullable=True),
        sa.Column("std_intensity", sa.Float(), nullable=True),
        sa.Column("z_score", sa.Float(), nullable=True),
        sa.Column("percent_effect", sa.Float(), nullable=True),
        sa.Column("raw_data", sa.JSON(), nullable=True),
        sa.Column("well_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["well_id"], ["wells.id"]),
    )


def downgrade() -> None:
    op.drop_table("analyses")
    op.drop_table("images")
    op.drop_table("wells")
    op.drop_index("ix_plates_barcode", "plates")
    op.drop_index("ix_plates_name", "plates")
    op.drop_table("plates")
    op.drop_index("ix_experiments_name", "experiments")
    op.drop_table("experiments")
    op.drop_index("ix_projects_name", "projects")
    op.drop_table("projects")
    op.drop_index("ix_compounds_identifier", "compounds")
    op.drop_table("compounds")
    op.drop_index("ix_users_email", "users")
    op.drop_table("users")
