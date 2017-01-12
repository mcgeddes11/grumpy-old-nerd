from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
order = Table('order', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('restaurant_id', Integer),
    Column('menu_id', Integer),
    Column('order_datetime', DateTime),
    Column('is_ready', Boolean),
    Column('is_completed', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['order'].columns['is_completed'].create()
    post_meta.tables['order'].columns['is_ready'].create()
    post_meta.tables['order'].columns['order_datetime'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['order'].columns['is_completed'].drop()
    post_meta.tables['order'].columns['is_ready'].drop()
    post_meta.tables['order'].columns['order_datetime'].drop()
