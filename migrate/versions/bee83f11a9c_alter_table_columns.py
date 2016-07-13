"""alter table columns

Revision ID: bee83f11a9c
Revises: 147d42584675
Create Date: 2016-07-06 11:02:10.379009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bee83f11a9c'
down_revision = '147d42584675'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.alter_column(
            'author', existing_type=sa.VARCHAR(), nullable=True)

    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('archived', sa.Boolean(), nullable=False))


def downgrade():
    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.drop_column('archived')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.alter_column(
            'author', existing_type=sa.VARCHAR(), nullable=False)
