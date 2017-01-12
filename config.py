import os, json
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True

# Get variables from env
# Note that current impl. is to have a single env. var which is JSON containing all the fields we need
vars = json.loads(os.getenv("BLOG_ENV_VARS"))

SECRET_KEY = vars["SECRET_KEY"]
MAIL_SERVER = vars["MAIL_SERVER"]
MAIL_PORT = vars["MAIL_PORT"]
MAIL_USERNAME = vars["MAIL_USERNAME"]
MAIL_PASSWORD = vars["MAIL_PASSWORD"]
MAIL_USE_TLS = bool(vars["MAIL_USE_TLS"]) # Encoded in env. JSON as "True" or "False" strings
MAIL_DEFAULT_SENDER = vars["MAIL_DEFAULT_SENDER"]


