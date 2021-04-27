"""Nova coluna Tamanhos

Revision ID: 935b240cacda
Revises: 712a951f6a14
Create Date: 2021-04-27 10:08:03.192707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '935b240cacda'
down_revision = '712a951f6a14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('produto', sa.Column('tamanhos', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('produto', 'tamanhos')
    # ### end Alembic commands ###
