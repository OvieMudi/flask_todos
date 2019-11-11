"""empty message

Revision ID: 506fb4eda870
Revises: 0481fe2b1023
Create Date: 2019-11-11 09:46:34.084859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '506fb4eda870'
down_revision = '0481fe2b1023'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('todos_todo_list_id_fkey1', 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'todolists', ['todo_list_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key('todos_todo_list_id_fkey1', 'todos', 'todolists', ['todo_list_id'], ['id'])
    # ### end Alembic commands ###
