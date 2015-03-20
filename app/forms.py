from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Length

class LoginForm(Form):
    kuid = StringField('kuid')
    password = PasswordField('password')
