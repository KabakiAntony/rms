"""added unique constraints to mobile and email

Revision ID: 3b769dfcbd6c
Revises: a361491516c3
Create Date: 2021-01-20 13:01:34.362358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b769dfcbd6c'
down_revision = 'a361491516c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Employees', ['email'])
    op.create_unique_constraint(None, 'Employees', ['mobile'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Employees', type_='unique')
    op.drop_constraint(None, 'Employees', type_='unique')
    # ### end Alembic commands ###
