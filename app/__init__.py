from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_misaka import Misaka
from flask_session import Session

app = Flask(__name__)
# Load config file from 'config.py'
app.config.from_object('config')

# Database
db = SQLAlchemy(app)

# Session
Session(app)

# Login manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Admin
adm = Admin(app)
#adm = Admin(app, app.config['NAME'], base_template='/admin/layout.html', template_mode='bootstrap3')

# Mail
mail = Mail(app)

# Text markdown
md = Misaka(wrap=True)
md.init_app(app)

from app import views
from app.user import views
from app.question import views
from app.log import views
from app.admin import views
