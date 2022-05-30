"""empty message

Revision ID: dea0267a9d99
Revises: 7b83ea7051ce
Create Date: 2022-05-26 11:14:06.970182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dea0267a9d99'
down_revision = '7b83ea7051ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Artist', sa.Column('looking_for_venue', sa.Boolean(), nullable=True))
    op.add_column('Artist', sa.Column('description', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('looking_for_venue', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'description')
    op.drop_column('Venue', 'looking_for_venue')
    op.drop_column('Venue', 'website_link')
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'description')
    op.drop_column('Artist', 'looking_for_venue')
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###