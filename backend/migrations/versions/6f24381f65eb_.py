"""empty message

Revision ID: 6f24381f65eb
Revises: 2084f23df2c4
Create Date: 2024-08-10 02:08:21.372967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f24381f65eb'
down_revision = '2084f23df2c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['User.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['follower_id'], ['User.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
