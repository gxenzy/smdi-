from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0d333fb631e3'
down_revision = None  # This is correct for the initial migration
branch_labels = None
depends_on = None

def upgrade():
    # Commands to upgrade the database schema
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )  # Closing parenthesis for create_table

def downgrade():
    # Commands to downgrade the database schema
    op.drop_table('users')  # This will drop the 'users' table created in upgrade