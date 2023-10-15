"""Populate Role table

Revision ID: f33d48e05427
Revises: 
Create Date: 2023-10-09 14:23:42.836481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f33d48e05427"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

role_table = sa.table(
    "role", sa.Column("id", sa.Integer, primary_key=True), sa.Column("name", sa.String)
)

roles_data = [
    {"id": 1, "name": "ADMIN"},
    {"id": 2, "name": "CUSTOMER"},
    {"id": 3, "name": "CANDIDATE"},
]


def upgrade() -> None:
    op.bulk_insert(role_table, roles_data)


def downgrade() -> None:
    op.execute(
        role_table.delete().where(
            role_table.c.id.in_([role["id"] for role in roles_data])
        )
    )
