from flask import url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user
from app import app, lm, db
from models import User
from forms import LoginForm, RegisterForm

@app.route('/')
@login_required
def index():
    return render_template('blank.html', message='Hello World!')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User.query.get(form.kuid.data)
        if u is None and form.password.data == form.repeat_password.data:
            u = User(form.kuid.data, form.password.data)
            db.session.add(u)
            db.session.commit()
            login_user(u)
            flash('Succesfully created user %s' % (u.kuid))
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.get(form.kuid.data)
        if u is not None and u.check_password(form.password.data):
            login_user(u)
            flash('Succesfully logged %s in' % (u.kuid))
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@lm.user_loader
def load_user(id):
    return User.query.get(id)
