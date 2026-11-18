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
    # Batch mode supports SQLite as well as PostgreSQL.
    with op.batch_alter_table("accommodations") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_accommodations_owner_id_users",
            "users",
            ["owner_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_index("ix_accommodations_owner_id", ["owner_id"])


def downgrade() -> None:
    with op.batch_alter_table("accommodations") as batch_op:
        batch_op.drop_index("ix_accommodations_owner_id")
        batch_op.drop_constraint(
            "fk_accommodations_owner_id_users",
            type_="foreignkey",
        )
        batch_op.drop_column("owner_id")
