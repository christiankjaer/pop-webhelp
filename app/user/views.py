from flask import url_for, redirect, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, lm, db
from models import User
from forms import LoginForm, RegisterForm, ChangePasswordForm
from token import confirm_token, generate_confirmation_token
from email import send_ku_email
import datetime

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    errors = []
    if form.validate_on_submit():
        # Look if the user is in the database.
        u = User.query.get(form.kuid.data)
        if u is None:
            if form.password.data == form.repeat_password.data:
                u = User(form.kuid.data, form.password.data)
                db.session.add(u)
                db.session.commit()

                token = generate_confirmation_token(u.kuid)
                confirm_url = url_for('confirm_account', token=token, _external=True)
                html = render_template('user/confirmation_mail.html', confirm_url=confirm_url)
                subject = 'Please confirm PoP-Webhelp account'
                send_ku_email(u.kuid, subject, html)

                flash('Succesfully created user %s. A confirmation mail has been sent' % (u.kuid))
                return redirect(url_for('login'))
            else:
                errors.append('Passwords must match')
        else:
            errors.append('User already exists')
    return render_template('user/register.html', form=form, errors=errors)

@app.route('/confirm/<token>')
def confirm_account(token):
    try:
        kuid = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    user = User.query.get(kuid)
    if user.confirmed:
        flash('Account already confirmed. Please login.')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Your account is confirmed')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.get(form.kuid.data)
        if u is not None and u.check_password(form.password.data):
            if u.confirmed:
                login_user(u)
                flash('Succesfully logged %s in' % (u.kuid))
                return redirect(url_for('index'))
            else:
                flash('Please confirm your account')
    return render_template('user/login.html', form=form)

@app.route('/changepw', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    errors = []
    if form.validate_on_submit():
        u = current_user
        if (form.password.data == form.repeat_password.data) and u.check_password(form.old_password.data):
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            flash('Password successfully changed')
            return redirect(url_for('index'))
        errors.append('Passwords must match')
    return render_template('user/changepw.html', form=form, errors=errors)

@app.route('/resetpw/<kuid>')
def request_password_reset(kuid):
    u = User.query.get(kuid)

    if u is not None:
        token = generate_confirmation_token(u.kuid)
        reset_url = url_for('reset_password', token=token, _external=True)
        html = render_template('user/reset_mail.html', reset_url=reset_url)
        subject = 'Your password reset link'
        send_ku_email(u.kuid, subject, html)
        flash('A reset link has been sent to your KU-mail')
    else:
        flash('User %s does not exist' % kuid)
    return redirect(url_for('index'))


@app.route('/reset/<token>')
def reset_password(token):
    try:
        kuid = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    user = User.query.get(kuid)
    if user is not None:
        newpw = user.reset_password()
        db.session.add(user)
        db.session.commit()
        html = render_template('user/password_mail.html', new_pw=newpw)
        subject = 'Your new password'
        send_ku_email(user.kuid, subject, html)
        flash('The new password has been sent')

    return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@lm.user_loader
def load_user(id):
    return User.query.get(id)
