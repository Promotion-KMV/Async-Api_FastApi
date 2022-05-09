"""empty message

Revision ID: 396bbb2378b4
Revises: f48d645d9adc
Create Date: 2022-05-06 18:59:40.361767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396bbb2378b4'
down_revision = 'f48d645d9adc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('oauth_type', sa.TEXT(), nullable=True), schema='auth')
    op.add_column('user', sa.Column('oauth_id', sa.TEXT(), nullable=True), schema='auth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'oauth_id', schema='auth')
    op.drop_column('user', 'oauth_type', schema='auth')
    # ### end Alembic commands ###