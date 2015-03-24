from flask_mail import Message

from app import app, mail

def send_ku_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to + app.config['USER_EMAIL_SUFFIX']],
        html = template,
        sender=app.config['MAIL_DEFAULT_SENDER'])
    msg.send(mail)
