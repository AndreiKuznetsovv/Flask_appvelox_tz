"""Task complition_date change

Revision ID: dccbdbd937fb
Revises: 2ab39decda0d
Create Date: 2023-03-25 17:05:34.558028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dccbdbd937fb'
down_revision = '2ab39decda0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('completion_date',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Date(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.alter_column('completion_date',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
