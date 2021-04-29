"""changed the fileUrl column to filename

Revision ID: 2054518b307d
Revises: ece38af5caf0
Create Date: 2021-04-29 15:41:26.738851

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2054518b307d'
down_revision = 'ece38af5caf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Budget')
    op.add_column('Files', sa.Column('fileName', sa.String(length=100), nullable=False))
    op.drop_column('Files', 'fileUrl')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Files', sa.Column('fileUrl', sa.VARCHAR(length=250), autoincrement=False, nullable=False))
    op.drop_column('Files', 'fileName')
    op.create_table('Budget',
    sa.Column('id', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('companyId', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('projectId', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], name='Budget_companyId_fkey'),
    sa.ForeignKeyConstraint(['projectId'], ['Project.id'], name='Budget_projectId_fkey'),
    sa.PrimaryKeyConstraint('id', name='Budget_pkey')
    )
    # ### end Alembic commands ###
