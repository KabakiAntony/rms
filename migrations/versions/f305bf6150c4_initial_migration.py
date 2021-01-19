"""initial migration

Revision ID: f305bf6150c4
Revises: 
Create Date: 2021-01-06 15:52:21.980853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f305bf6150c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Company',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('company', sa.String(length=64), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Company_company'), 'Company', ['company'], unique=True)
    op.create_table('Project',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('project_name', sa.String(length=100), nullable=False),
    sa.Column('companyId', sa.String(length=20), nullable=True),
    sa.Column('date_from', sa.Date(), nullable=True),
    sa.Column('date_to', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('project_name')
    )
    op.create_table('Users',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('companyId', sa.String(length=20), nullable=True),
    sa.Column('role', sa.String(length=25), nullable=False),
    sa.Column('isActive', sa.String(length=25), nullable=False),
    sa.ForeignKeyConstraint(['companyId'], ['Company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Users_email'), 'Users', ['email'], unique=True)
    op.create_index(op.f('ix_Users_username'), 'Users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Users_username'), table_name='Users')
    op.drop_index(op.f('ix_Users_email'), table_name='Users')
    op.drop_table('Users')
    op.drop_table('Project')
    op.drop_index(op.f('ix_Company_company'), table_name='Company')
    op.drop_table('Company')
    # ### end Alembic commands ###