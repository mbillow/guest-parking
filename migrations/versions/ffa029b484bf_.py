"""empty message

Revision ID: ffa029b484bf
Revises: e875f7afe573
Create Date: 2018-11-06 00:18:52.244481

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ffa029b484bf'
down_revision = 'e875f7afe573'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('cancelled', sa.Boolean(), nullable=False))
    op.drop_column('booking', 'registered')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('registered', mysql.VARCHAR(length=60), nullable=True))
    op.drop_column('booking', 'cancelled')
    # ### end Alembic commands ###