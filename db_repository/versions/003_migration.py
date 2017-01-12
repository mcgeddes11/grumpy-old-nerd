from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=50)),
    Column('first_name', VARCHAR(length=50)),
    Column('last_name', VARCHAR(length=50)),
    Column('street_address', VARCHAR(length=150)),
    Column('city', VARCHAR(length=60)),
    Column('province', VARCHAR(length=2)),
    Column('postal_code', VARCHAR(length=6)),
    Column('signup_datetime', DATETIME),
    Column('lat', FLOAT),
    Column('long', FLOAT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['long'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['long'].create()
