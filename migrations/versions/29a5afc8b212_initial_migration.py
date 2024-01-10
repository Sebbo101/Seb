"""Initial migration

Revision ID: 29a5afc8b212
Revises: 
Create Date: 2024-01-09 22:31:43.568181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29a5afc8b212'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('airline', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('flight_number', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('registration', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('departure_airport', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('arrival_airport', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('aircraft_type', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('departure_delay', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('aircraft_cleanliness', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('friendliness', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('entertainment_quality', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('food_quality', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('user_friendliness', sa.Integer(), nullable=False))
        batch_op.drop_column('comment')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('user_friendliness')
        batch_op.drop_column('food_quality')
        batch_op.drop_column('entertainment_quality')
        batch_op.drop_column('friendliness')
        batch_op.drop_column('aircraft_cleanliness')
        batch_op.drop_column('departure_delay')
        batch_op.drop_column('aircraft_type')
        batch_op.drop_column('arrival_airport')
        batch_op.drop_column('departure_airport')
        batch_op.drop_column('registration')
        batch_op.drop_column('flight_number')
        batch_op.drop_column('airline')

    # ### end Alembic commands ###