from app import db, app
from flask import request
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
import bleach
import flask_whooshalchemy as whooshalchemy
enable_search = True



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(140))
    last_name = db.Column(db.String(140))
    urole = db.Column(db.String(80))
    avatar_hash = db.Column(db.String(32))
    pw_reset_guid = db.Column(db.String(36))
    pw_reset_expiry = db.Column(db.DateTime)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, email, formdata=None):
        self.email = email
        self.signup_datetime = datetime.utcnow()
        if formdata is not None:
            self.password = formdata.password.data
            self.first_name = formdata.first_name.data
            self.last_name = formdata.last_name.data
            # TODO: better way to allocate this
            self.urole = "user"
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode("utf-8")).hexdigest()

    def gravatar(self, size=100,default="identicon", rating="g"):
        if request.is_secure:
            url = "https://secure.gravatar.com/avatar"
        else:
            url = "http://www.gravatar.com/avatar"
        hash = self.avatar_hash or hashlib.md5(self.email.encode("utf-8")).hexdigest()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(url=url,hash=hash,size=size,default=default,rating=rating)

    @property
    def password(self):
        raise AttributeError("'password' is not a readable attribute")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def get_urole(self):
        return self.urole

    def __repr__(self):
        return '<User %r>' % (self.email)


class Post(db.Model):
    __tablename__ = "posts"
    __searchable__ = ["title","body"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_published = db.Column(db.Boolean)

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author
        self.is_published = False
        self.timestamp = datetime.utcnow()

    @staticmethod
    def on_changed_body(target, value, old_value, initiator):
        allowed_tags = ['a','abbr','acronym','b','blockquote','code','div','em','i','img','li','ol','pre','src','strong','ul','h1','h2','h3','p']
        allowed_attributes = ['src','href','style','class','name','id']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),tags=allowed_tags,attributes=allowed_attributes,strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)
if enable_search:
    whooshalchemy.whoosh_index(app, Post)
