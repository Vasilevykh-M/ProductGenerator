"""initial

Revision ID: cedb8c11fc81
Revises: 
Create Date: 2024-09-20 15:24:43.589707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cedb8c11fc81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('promt', 'name_object',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('promt', 'promt',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('promt', 'promt',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('promt', 'name_object',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
    # ### end Alembic commands ###
