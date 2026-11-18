"""Add an optional owner to accommodation listings.

Revision ID: 0004_add_accommodation_owner
Revises: 0003_create_users
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_add_accommodation_owner"
down_revision: Union[str, None] = "0003_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "accommodations",
        sa.Column("owner_id", sa.Integer(), nullable=True),
    )
    op.create_index(
        "ix_accommodations_owner_id",
        "accommodations",
        ["owner_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_accommodations_owner_id_users",
        "accommodations",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_accommodations_owner_id_users",
        "accommodations",
        type_="foreignkey",
    )
    op.drop_index("ix_accommodations_owner_id", table_name="accommodations")
    op.drop_column("accommodations", "owner_id")
