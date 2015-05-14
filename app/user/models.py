import datetime
from app import db
from app.question.models import Subject
from werkzeug.security import generate_password_hash, check_password_hash
from string import ascii_uppercase, digits
from random import SystemRandom

class User(db.Model):
    """This class represents a user"""
    kuid = db.Column(db.String(6), primary_key=True)
    pwhash = db.Column(db.String(160), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    completed = db.relationship('Subject', secondary=lambda: completed,
                                backref=db.backref('users', lazy='dynamic'))

    def __init__(self, kuid, password, confirmed=False, confirmed_on=None):
        self.kuid = kuid
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.set_password(password)

    def __repr__(self):
        return '<User %s>' % (self.kuid)

    def check_password(self, password):
        """Checks the password against the stored"""
        return check_password_hash(self.pwhash, password)

    def set_password(self, password):
        """Sets the users password"""
        self.pwhash = generate_password_hash(password)

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
        """Generate a random password with 10 characters"""
        return ''.join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(10))

# Many-to-many table
completed = db.Table('completed',
                     db.Column('kuid', db.String(6), db.ForeignKey('user.kuid'), primary_key=True),
                     db.Column('sname', db.String(50), db.ForeignKey('subject.name'), primary_key=True))
