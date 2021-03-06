from flask_mail import Message

from app import app, mail

def send_ku_email(to, subject, template):
    """Sends an email to the KU-mail associated with the user"""
    msg = Message(
        subject,
        recipients=[to + app.config['USER_EMAIL_SUFFIX']],
        html = template,
        sender=app.config['MAIL_DEFAULT_SENDER'])
    if not app.config['TESTING']:
        msg.send(mail)
