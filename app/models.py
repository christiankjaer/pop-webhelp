import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    kuid = db.Column(db.String(6), primary_key=True)
    pwhash = db.Column(db.String(160), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, kuid, password, confirmed=False, confirmed_on=None):
        self.kuid = kuid
        self.pwhash = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self):
        return '<User %r>' % (self.kuid)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def is_active(self):
        return self.confirmed

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.kuid
