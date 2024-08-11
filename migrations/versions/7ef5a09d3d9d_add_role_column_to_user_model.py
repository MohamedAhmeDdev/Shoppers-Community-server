from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision = '7ef5a09d3d9d'
down_revision = None
branch_labels = None
depends_on = None

def get_column_names(table_name):
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)
    columns = inspector.get_columns(table_name)
    return [column['name'] for column in columns]

def upgrade():
    # Check if the column already exists
    if 'role' not in get_column_names('users'):
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=False, server_default='user'))

def downgrade():
    # Check if the column exists before dropping it
    if 'role' in get_column_names('users'):
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.drop_column('role')
