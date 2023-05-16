"""create account table

Revision ID: e8708387f12d
Revises: 
Create Date: 2023-05-16 17:27:14.293458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e8708387f12d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "phone",
            sa.Integer,
            nullable=False,
            autoincrement=False,
            info={"min_digits": 10, "max_digits": 10},
        ),
    )

    op.create_table(
        "profile",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("profile_picture", sa.LargeBinary, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("profile")
