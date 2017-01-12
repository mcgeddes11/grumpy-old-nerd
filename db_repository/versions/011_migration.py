from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menuitem = Table('menuitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('menu_id', Integer),
    Column('item_name', String(length=40)),
    Column('item_desc', String(length=140)),
    Column('item_price', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menuitem'].columns['item_price'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menuitem'].columns['item_price'].drop()
