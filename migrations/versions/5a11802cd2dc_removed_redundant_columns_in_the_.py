"""removed redundant columns in the detailedFiles table

Revision ID: 5a11802cd2dc
Revises: fdfdb3d7f35b
Create Date: 2021-05-31 10:49:37.046262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a11802cd2dc'
down_revision = 'fdfdb3d7f35b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('DetailedFile_projectId_fkey', 'DetailedFile', type_='foreignkey')
    op.drop_constraint('DetailedFile_companyId_fkey', 'DetailedFile', type_='foreignkey')
    op.drop_column('DetailedFile', 'fileType')
    op.drop_column('DetailedFile', 'companyId')
    op.drop_column('DetailedFile', 'projectId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('DetailedFile', sa.Column('projectId', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('DetailedFile', sa.Column('companyId', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.add_column('DetailedFile', sa.Column('fileType', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.create_foreign_key('DetailedFile_companyId_fkey', 'DetailedFile', 'Company', ['companyId'], ['id'])
    op.create_foreign_key('DetailedFile_projectId_fkey', 'DetailedFile', 'Project', ['projectId'], ['id'])
    # ### end Alembic commands ###
