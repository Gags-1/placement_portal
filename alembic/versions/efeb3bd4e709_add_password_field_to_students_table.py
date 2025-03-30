"""Add password field to students table

Revision ID: efeb3bd4e709
Revises: c969ff2abc02
Create Date: 2025-03-11 00:48:14.392336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efeb3bd4e709'
down_revision: Union[str, None] = 'c969ff2abc02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('students', sa.Column('password', sa.String(), nullable=True))  # Allow NULL first
    op.execute("UPDATE students SET password = 'default_password'")  # Set a default password for existing rows
    op.alter_column('students', 'password', nullable=False)    


def downgrade() -> None:
    op.drop_column('students', 'password')