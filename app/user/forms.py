from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Regexp, DataRequired

class LoginForm(Form):
    kuid = StringField('kuid', validators=[DataRequired(), Regexp('[a-z]{3}[0-9]{3}', message = 'Wrong format!')])
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(Form):
    kuid = StringField('kuid', validators=[DataRequired(), Regexp('[a-z]{3}[0-9]{3}', message = 'Wrong format!')])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('password', validators=[DataRequired()])

class ChangePasswordForm(Form):
    old_password = PasswordField('password', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    repeat_password = PasswordField('password', validators=[DataRequired()])

class RequestPasswordResetForm(Form):
    kuid = StringField('kuid', validators=[DataRequired()])
