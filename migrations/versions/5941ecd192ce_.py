"""empty message

Revision ID: 5941ecd192ce
Revises: 
Create Date: 2024-08-09 15:43:56.797680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5941ecd192ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
