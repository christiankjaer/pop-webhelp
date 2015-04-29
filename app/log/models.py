import datetime
from app import db
from app.question.models import Question, Subject
from app.user.models import User

class QLog(db.Model):
    __tablename__ = 'qlog'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    qid = db.Column(db.Integer, db.ForeignKey('question.id'))
    uid = db.Column(db.String(6), db.ForeignKey('user.kuid'))
    sid = db.Column(db.Integer, db.ForeignKey('session.id'))
    answer = db.Column(db.Text())
    correct = db.Column(db.Boolean)

    def __init__(self, qid, uid, sid, answer, correct):
        self.date = datetime.datetime.now()
        self.qid = qid
        self.uid = uid
        self.sid = sid
        self.answer = answer
        self.correct = correct

    def __repr__(self):
        return 'QLog %s' % (self.id)

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    uid = db.Column(db.String(6), db.ForeignKey('user.kuid'))
    sname = db.Column(db.String(50), db.ForeignKey('subject.name'))
    logs = db.relationship('QLog', backref='session')

    def __init__(self, uid, sname):
        self.date = datetime.datetime.now()
        self.uid = uid
        self.sname = sname
        
    def __repr__(self):
        return 'Sessions %s' % (self.id)
