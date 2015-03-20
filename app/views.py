from flask import url_for, redirect, render_template
from flask_login import login_user
from app import app, lm, db
from models import User
from forms import LoginForm

@app.route('/')
def index():
    return "Hello World!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print form.kuid.data
        u = User.query.get(form.kuid.data)
        if u.check_password(form.password.data):
            login_user(u)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(id)
