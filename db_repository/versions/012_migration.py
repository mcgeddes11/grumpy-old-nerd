from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=50)),
    Column('first_name', String(length=50)),
    Column('last_name', String(length=50)),
    Column('street_address', String(length=150)),
    Column('city', String(length=60)),
    Column('province', String(length=2)),
    Column('postal_code', String(length=6)),
    Column('phone_number', String(length=15)),
    Column('signup_datetime', DateTime),
    Column('lat', Float),
    Column('long', Float),
)

restaurant = Table('restaurant', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120), primary_key=True, nullable=False),
    Column('password', String(length=50)),
    Column('business_name', String(length=100)),
    Column('street_address', String(length=150)),
    Column('city', String(length=60)),
    Column('province', String(length=2)),
    Column('postal_code', String(length=6)),
    Column('phone_number', String(length=15)),
    Column('signup_datetime', DateTime),
    Column('lat', Float),
    Column('long', Float),
    Column('order_minimum', Float),
    Column('deliver_radius', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['phone_number'].create()
    post_meta.tables['restaurant'].columns['phone_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['phone_number'].drop()
    post_meta.tables['restaurant'].columns['phone_number'].drop()
