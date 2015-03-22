from flask_mail import Message

from app import app, mail

def send_ku_email(to, subject, template):
    msg = Message(
        subject,
        recipients=["%s@alumni.ku.dk" % to],
        html = template,
        sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)
