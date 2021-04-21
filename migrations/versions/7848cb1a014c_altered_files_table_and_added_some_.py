"""altered files table and added some columns

Revision ID: 7848cb1a014c
Revises: 92d74c965e5f
Create Date: 2021-04-13 12:33:42.361520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7848cb1a014c'
down_revision = '92d74c965e5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Files', sa.Column('authorizedOrRejectedBy', sa.String(length=20), nullable=True))
    op.add_column('Files', sa.Column('fileAmount', sa.Float(), nullable=False))
    op.add_column('Files', sa.Column('fileType', sa.String(length=10), nullable=False))
    op.add_column('Files', sa.Column('fileVersion', sa.String(length=2), nullable=False))
    op.drop_constraint('Files_authorizedBy_fkey', 'Files', type_='foreignkey')
    op.create_foreign_key(None, 'Files', 'Users', ['authorizedOrRejectedBy'], ['id'])
    op.drop_column('Files', 'authorizedBy')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Files', sa.Column('authorizedBy', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Files', type_='foreignkey')
    op.create_foreign_key('Files_authorizedBy_fkey', 'Files', 'Users', ['authorizedBy'], ['id'])
    op.drop_column('Files', 'fileVersion')
    op.drop_column('Files', 'fileType')
    op.drop_column('Files', 'fileAmount')
    op.drop_column('Files', 'authorizedOrRejectedBy')
    # ### end Alembic commands ###
