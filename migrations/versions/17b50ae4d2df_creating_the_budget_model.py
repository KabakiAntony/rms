"""creating the budget model

Revision ID: 17b50ae4d2df
Revises: 68be880f1f35
Create Date: 2020-10-01 11:45:38.499853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b50ae4d2df'
down_revision = '68be880f1f35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Budget',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('companyId', sa.Integer(), nullable=True),
    sa.Column('projectId', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['projectId'], ['Project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Budget')
    # ### end Alembic commands ###
