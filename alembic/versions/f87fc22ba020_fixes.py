"""fixes

Revision ID: f87fc22ba020
Revises: b8b6a26fa480
Create Date: 2025-12-10 10:34:39.210868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f87fc22ba020'
down_revision: Union[str, Sequence[str], None] = 'b8b6a26fa480'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("tasks") as batch:
        batch.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch.create_foreign_key(
            "fk_tasks_user_id",
            "user",
            ["user_id"],
            ["id"],
        )
    # если хотите NOT NULL, и таблица пустая: сразу nullable=False.
    # если есть данные — сначала nullable=True, заполнить, потом отдельной
    # миграцией ужесточить.


def downgrade():
    with op.batch_alter_table("tasks") as batch:
        batch.drop_constraint("fk_tasks_user_id", type_="foreignkey")
        batch.drop_column("user_id")