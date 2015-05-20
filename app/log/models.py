import datetime
from app import db
from app.question.models import Question, Subject, Hint
from app.user.models import User

class QLog(db.Model):
    __tablename__ = 'qlog'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    qid = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question')
    uid = db.Column(db.String(6), db.ForeignKey('users.kuid'))
    sid = db.Column(db.String(60))
    answer = db.Column(db.Text())
    correct = db.Column(db.Boolean)
    hints = db.Column(db.Integer)

    def __init__(self, session):
        self.date = datetime.datetime.now()
        self.qid = session['qid']
        self.uid = session['uid']
        self.sid = session['sid']
        self.answer = session['answer']
        self.correct = session['correct']
        self.hints = len(session['hints'])

    def __repr__(self):
        return 'QLog %s' % (self.id)

class HintRating(db.Model):
    __tablename__ = 'hint_rating'
    id = db.Column(db.Integer, primary_key=True)
    hid = db.Column(db.Integer, db.ForeignKey('hint.id'))
    rating = db.Column(db.String(255))

    def __init__(self, hid, rating):
        self.hid = hid
        self.rating = rating
    def __repr__(self):
        return 'HintRating %s' % (self.id)
