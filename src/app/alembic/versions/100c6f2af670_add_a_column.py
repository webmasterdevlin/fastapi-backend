"""Add a column

Revision ID: 100c6f2af670
Revises: 8c68f4c16a17
Create Date: 2024-04-26 08:38:21.010100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '100c6f2af670'
down_revision: Union[str, None] = '8c68f4c16a17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
