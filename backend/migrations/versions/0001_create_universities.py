"""Create the universities table.

Revision ID: 0001_create_universities
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_create_universities"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "universities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("slug", sa.String(length=160), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("institution_type", sa.String(length=30), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_universities_id", "universities", ["id"], unique=False)
    op.create_index("ix_universities_name", "universities", ["name"], unique=True)
    op.create_index("ix_universities_slug", "universities", ["slug"], unique=True)
    op.create_index("ix_universities_state", "universities", ["state"], unique=False)
    op.create_index(
        "ix_universities_institution_type",
        "universities",
        ["institution_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_universities_institution_type", table_name="universities")
    op.drop_index("ix_universities_state", table_name="universities")
    op.drop_index("ix_universities_slug", table_name="universities")
    op.drop_index("ix_universities_name", table_name="universities")
    op.drop_index("ix_universities_id", table_name="universities")
    op.drop_table("universities")
