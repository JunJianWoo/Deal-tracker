"""Initial schema

Revision ID: 06b2f26cbdf8
Revises: 
Create Date: 2025-06-21 00:22:59.648304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06b2f26cbdf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fetch_history',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('items_created', sa.Integer(), nullable=False),
    sa.Column('item_prices_created', sa.Integer(), nullable=False),
    sa.Column('websites_failed', sa.JSON(), nullable=False),
    sa.Column('successful_scrapes', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('date')
    )
    op.create_table('item',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('image_link', sa.String(length=400), nullable=False),
    sa.Column('website_link', sa.String(length=400), nullable=False),
    sa.Column('company_source', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_price',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('original_price', sa.Integer(), nullable=False),
    sa.Column('discounted_price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['item.id'], ),
    sa.PrimaryKeyConstraint('id', 'date')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_price')
    op.drop_table('item')
    op.drop_table('fetch_history')
    # ### end Alembic commands ###
