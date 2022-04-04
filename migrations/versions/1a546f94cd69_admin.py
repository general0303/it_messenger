"""admin

Revision ID: 1a546f94cd69
Revises: b09639722f8a
Create Date: 2022-04-04 12:42:04.078709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a546f94cd69'
down_revision = 'b09639722f8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chat', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chat', type_='foreignkey')
    op.drop_column('chat', 'user_id')
    # ### end Alembic commands ###
