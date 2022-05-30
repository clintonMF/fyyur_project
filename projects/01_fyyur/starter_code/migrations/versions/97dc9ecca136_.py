"""empty message

Revision ID: 97dc9ecca136
Revises: 4e8fe0cead56
Create Date: 2022-05-26 23:08:41.168544

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '97dc9ecca136'
down_revision = '4e8fe0cead56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.String(), nullable=True))
    op.drop_column('artist', 'description')
    op.add_column('show', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.drop_column('show', 'datetime')
    op.add_column('venue', sa.Column('seeking_description', sa.String(), nullable=True))
    op.drop_column('venue', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('venue', 'seeking_description')
    op.add_column('show', sa.Column('datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('show', 'start_time')
    op.add_column('artist', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###
