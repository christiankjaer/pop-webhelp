from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
# Load config file from 'config.py'
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()

from app import views
