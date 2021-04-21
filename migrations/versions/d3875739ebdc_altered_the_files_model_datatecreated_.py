"""altered the files model datateCreated and dateAuthorized columns

Revision ID: d3875739ebdc
Revises: 2d7c62bc62ab
Create Date: 2021-04-19 13:14:41.975645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3875739ebdc'
down_revision = '2d7c62bc62ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Files', sa.Column('dateCreated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Files', 'dateCreated')
    # ### end Alembic commands ###
