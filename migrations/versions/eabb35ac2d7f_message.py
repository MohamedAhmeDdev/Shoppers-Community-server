"""message

Revision ID: eabb35ac2d7f
Revises: 
Create Date: 2024-08-04 18:30:59.945592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eabb35ac2d7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('searches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('searches', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###