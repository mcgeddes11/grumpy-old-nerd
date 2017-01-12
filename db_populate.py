# TODO:  Write a script to populate some test data.  Should include:
'''
- 2 Users, one admin, one regular
- 2 test posts for each user
'''

from app import db
from datetime import datetime
from app.models import User, Post
from random import seed, randint
import forgery_py

# User 1 - admin
u1 = User("testadmin@email.com")
u1.password = "password"
u1.first_name = "Test"
u1.last_name = "Admin"
u1.urole = "admin"
db.session.add(u1)


# User 2 - user
u2 = User("testuser@user.com")
u2.password = "password"
u2.first_name = "Test"
u2.last_name = "User"
u2.urole = "user"
db.session.add(u2)

db.session.commit()

# N posts for testing
count = 20
user_count = User.query.count()
for i in range(count):
    u = User.query.offset(randint(0,user_count-1)).first()
    p = Post(title=forgery_py.lorem_ipsum.words(10), body=forgery_py.lorem_ipsum.sentences(randint(1,5)), author=u)
    p.timestamp = forgery_py.date.date(True)
    p.is_published = randint(0,1)
    db.session.add(p)
    db.session.commit()
