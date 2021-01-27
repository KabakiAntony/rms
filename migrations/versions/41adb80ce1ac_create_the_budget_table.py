"""create the budget table

Revision ID: 41adb80ce1ac
Revises: 3b769dfcbd6c
Create Date: 2021-01-27 19:09:16.346925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41adb80ce1ac'
down_revision = '3b769dfcbd6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Budget',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('companyId', sa.String(length=20), nullable=True),
    sa.Column('projectId', sa.String(length=20), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('fileUrl', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], ),
    sa.ForeignKeyConstraint(['projectId'], ['Project.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fileUrl')
    )
    


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Employees',
    sa.Column('id', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('companyId', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('firstname', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('lastname', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('mobile', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], name='Employees_companyId_fkey'),
    sa.PrimaryKeyConstraint('id', name='Employees_pkey'),
    sa.UniqueConstraint('email', name='Employees_email_key'),
    sa.UniqueConstraint('mobile', name='Employees_mobile_key')
    )
    op.drop_table('Budget')
    # ### end Alembic commands ###
