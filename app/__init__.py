from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin

app = Flask(__name__)
# Load config file from 'config.py'
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

adm = Admin(app)
mail = Mail(app)

from app import views
from app.user import views
from app.question import views
from app.log import views
from app.admin import views
