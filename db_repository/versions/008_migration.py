from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('restaurant_id', Integer),
    Column('menuitem_id', Integer),
    Column('created_datetime', DateTime),
    Column('is_active', Boolean),
)

menuitem = Table('menuitem', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('menu_id', Integer),
    Column('item_name', String(length=40)),
    Column('item_desc', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].create()
    post_meta.tables['menuitem'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].drop()
    post_meta.tables['menuitem'].drop()
