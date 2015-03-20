from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Length

class LoginForm(Form):
    kuid = StringField('kuid', validators=[Length(min=1, max=6)])
    password = PasswordField('password')
