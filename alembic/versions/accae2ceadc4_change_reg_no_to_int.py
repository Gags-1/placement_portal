"""change reg no to int

Revision ID: accae2ceadc4
Revises: efeb3bd4e709
Create Date: 2025-03-11 02:09:01.915424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'accae2ceadc4'
down_revision: Union[str, None] = 'efeb3bd4e709'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
      op.alter_column(
        'students', 
        'registration_no',
        type_=sa.Integer,
        existing_type=sa.String,
        postgresql_using="registration_no::integer"  # This ensures safe conversion
    )


def downgrade() -> None:
       # Revert registration_no column back to STRING (VARCHAR) if needed
    op.alter_column(
        'students', 
        'registration_no',
        type_=sa.String,
        existing_type=sa.Integer
    )