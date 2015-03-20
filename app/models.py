from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    kuid = db.Column(db.String(6), primary_key=True)
    pwhash = db.Column(db.String(160))

    def __init__(self, kuid, password):
        self.kuid = kuid
        self.pwhash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % (self.kuid)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
