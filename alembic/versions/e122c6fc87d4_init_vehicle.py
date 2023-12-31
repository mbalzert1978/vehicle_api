"""
init vehicle.

Revision ID: e122c6fc87d4
Revises:
Create Date: 2023-06-22 23:01:34.967620
"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e122c6fc87d4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vehicle",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("year_of_manufacture", sa.Integer(), nullable=False),
        sa.Column("body", sa.JSON(), nullable=False),
        sa.Column("ready_to_drive", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vehicle")
    # ### end Alembic commands ###
