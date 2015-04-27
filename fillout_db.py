from app import db
from app.user.models import User
from app.question.models import *

user = User('abc123', 'pwd', confirmed=True)

t1 = Threshold('Test Threshold 1', 2)
t2 = Threshold('Test Threshold 2')

s1 = Subject('TypeIn Subject', 'This is Test Subject 1', 1)
s2 = Subject('Multiple Choice Subject', 'This is Test Subject 2', 1)
s3 = Subject('Ranking Subject', 'This is Test Subject 3', 1)

tiq = {'type':'TypeIn', 'text':'What is 2 + 2?', 'subject':'TypeIn Subject',
       'answer':'4'}
q1 = Question.from_dict(tiq)

mcq = {'type':'MultipleChoice', 'text':'What is 2 + 2?', 
       'subject':'Multiple Choice Subject',
       'answer':[{'text':'3', 'correct':False}, 
                 {'text':'4', 'correct':True}, 
                 {'text':'5', 'correct':False}]}
q2 = Question.from_dict(mcq)

rkq = {'type':'Ranking', 'text':'Rank these numbers', 
       'subject':'Ranking Subject',
       'items':['1', '2', '3']}
q3 = Question.from_dict(rkq)

db.session.add(user)
db.session.add(t1)
db.session.add(t2)
db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.add(q1)
db.session.add(q2)
db.session.add(q3)
db.session.commit()
