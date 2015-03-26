import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from string import ascii_uppercase, digits
from random import SystemRandom

class User(db.Model):
    kuid = db.Column(db.String(6), primary_key=True)
    pwhash = db.Column(db.String(160), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, kuid, password, confirmed=False, confirmed_on=None):
        self.kuid = kuid
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % (self.kuid)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def set_password(self, password):
        self.pwhash = generate_password_hash(password)

    def reset_password(self):
        newpw = ''.join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(10))
        self.set_password(newpw)
        return newpw

    def is_active(self):
        return self.confirmed

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.kuid

    @staticmethod
    def random_password():
        return ''.join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(10))
