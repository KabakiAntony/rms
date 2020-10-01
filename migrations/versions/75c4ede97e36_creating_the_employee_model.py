"""creating the employee model

Revision ID: 75c4ede97e36
Revises: 17b50ae4d2df
Create Date: 2020-10-01 12:19:29.510267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75c4ede97e36'
down_revision = '17b50ae4d2df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=120), nullable=False),
    sa.Column('lastname', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('companyId', sa.Integer(), nullable=True),
    sa.Column('project', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['project'], ['Project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Employees')
    # ### end Alembic commands ###
