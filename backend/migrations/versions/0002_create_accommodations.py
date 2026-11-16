"""Create the accommodations table.

Revision ID: 0002_create_accommodations
Revises: 0001_create_universities
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_create_accommodations"
down_revision: Union[str, None] = "0001_create_universities"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "accommodations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("accommodation_type", sa.String(length=40), nullable=False),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("price_period", sa.String(length=20), nullable=False),
        sa.Column("area", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column(
            "university_id",
            sa.Integer(),
            sa.ForeignKey("universities.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "is_available",
            sa.Boolean(),
            server_default=sa.true(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "price > 0",
            name="ck_accommodations_price_positive",
        ),
    )
    op.create_index("ix_accommodations_id", "accommodations", ["id"])
    op.create_index("ix_accommodations_title", "accommodations", ["title"])
    op.create_index(
        "ix_accommodations_accommodation_type",
        "accommodations",
        ["accommodation_type"],
    )
    op.create_index("ix_accommodations_area", "accommodations", ["area"])
    op.create_index(
        "ix_accommodations_university_id",
        "accommodations",
        ["university_id"],
    )
    op.create_index(
        "ix_accommodations_is_available",
        "accommodations",
        ["is_available"],
    )


def downgrade() -> None:
    op.drop_index("ix_accommodations_is_available", table_name="accommodations")
    op.drop_index("ix_accommodations_university_id", table_name="accommodations")
    op.drop_index("ix_accommodations_area", table_name="accommodations")
    op.drop_index(
        "ix_accommodations_accommodation_type",
        table_name="accommodations",
    )
    op.drop_index("ix_accommodations_title", table_name="accommodations")
    op.drop_index("ix_accommodations_id", table_name="accommodations")
    op.drop_table("accommodations")
