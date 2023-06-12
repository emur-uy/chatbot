"""create information table

Revision ID: 3d80eb9c33cd
Revises:
Create Date: 2023-06-12 13:33:03.190462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d80eb9c33cd'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'information',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url', sa.String, nullable=False),
        sa.Column('data', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=False), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Agregar restricción de unicidad a la columna 'url'
    op.create_unique_constraint('uq_information_url', 'information', ['url'])

def downgrade():
    op.drop_constraint('uq_information_url', 'information', type_='unique')
    op.drop_table('information')