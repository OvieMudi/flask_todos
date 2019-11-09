"""empty message

Revision ID: b67e1b15ad90
Revises: 
Create Date: 2019-11-08 09:03:22.350539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b67e1b15ad90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    op.drop_column('todos', 'title')
    op.execute(
        'UPDATE todos SET completed = False WHERE completed IS NULL')

    op.alter_column('todos', 'completed', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('title', sa.VARCHAR(),
                                     autoincrement=False, nullable=False))
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
