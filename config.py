import os, json
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True

WHOOSH_BASE = os.path.join(basedir,"whoosh_index")
MAIL_SERVER = "smtp-mail.outlook.com"
MAIL_PORT = 587
MAIL_USE_TLS = True

# Get variables from env
SECRET_KEY = os.getenv("BLOG_SECRET_KEY")
MAIL_USERNAME = os.getenv("BLOG_MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("BLOG_MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.getenv("BLOG_MAIL_DEFAULT_SENDER")


