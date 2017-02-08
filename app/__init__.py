from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_wtf import csrf
import platform, sys
from utils import LoggerWriter

app = Flask(__name__)
app.config.from_object('config')
csrf.CsrfProtect(app)
mail = Mail(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
pagedown = PageDown()
pagedown.init_app(app)


import logging
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('tmp/grumpy_old_nerd.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('grumpy_old_nerd startup')
sys.stdout = LoggerWriter(app.logger.info)
sys.stderr = LoggerWriter(app.logger.warning)

from app import views, models