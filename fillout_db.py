from app import db
from app.user.models import User
from app.question.models import *

user = User('abc123', 'pwd', confirmed=True)
db.session.add(user)

thres = {'name':'Empty Threshold'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Matching Threshold', 'next':'Empty Threshold'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Ranking Threshold', 'next':'Matching Threshold'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Multiple Choice Threshold', 'next':'Ranking Threshold'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'TypeIn Threshold', 'next':'Multiple Choice Threshold'}
db.session.add(Threshold.from_dict(thres))

sub = {'name':'TypeIn Subject', 'text':'This is Test Subject 1', 
      'threshold':'TypeIn Threshold', 'goal':4}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Multiple Choice Subject', 'text':'This is Test Subject 2', 
       'threshold':'Multiple Choice Threshold', 'goal':3}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Ranking Subject', 'text':'This is Test Subject 3', 
       'threshold':'Ranking Threshold', 'goal':2}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Matching Subject', 'text':'This is Test Subject 4', 
       'threshold':'Matching Threshold', 'goal':2}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Empty Subject', 'text':'This is Test Subject 5', 
       'threshold':'Empty Threshold', 'goal':2}
db.session.add(Subject.from_dict(sub))

tiq = {'type':'TypeIn', 'text':'What is 2 + 2?', 'subject':'TypeIn Subject',
       'answer':'4',
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
db.session.add(Question.from_dict(tiq))

tiq = {'type':'TypeIn', 'text':'What is 2 - 2?', 'subject':'TypeIn Subject',
       'answer':'0',
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
db.session.add(Question.from_dict(tiq))

tiq = {'type':'TypeIn', 'text':'What is 2 * 2?', 'subject':'TypeIn Subject',
       'answer':'4',
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
db.session.add(Question.from_dict(tiq))

tiq = {'type':'TypeIn', 'text':'What is 2 / 2?', 'subject':'TypeIn Subject',
       'answer':'1',
       'hints': ['Hint1', 'Hint2'],
       'weight': 2}
db.session.add(Question.from_dict(tiq))

mcq = {'type':'MultipleChoice', 'text':'What is 2 + 2?',
       'subject':'Multiple Choice Subject',
       'choices':[{'text':'3', 'correct':False},
                 {'text':'5', 'correct':False},
                 {'text':'4', 'correct':True},
                 {'text':'6', 'correct':False}],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1, 'mctype': '1'}
db.session.add(Question.from_dict(mcq))

mcq = {'type':'MultipleChoice', 'text':'What is 2 - 2?',
       'subject':'Multiple Choice Subject',
       'choices':[{'text':'-2', 'correct':False},
                 {'text':'0', 'correct':True},
                 {'text':'2', 'correct':False},
                 {'text':'4', 'correct':False}],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1, 'mctype': 'X'}
db.session.add(Question.from_dict(mcq))

mcq = {'type':'MultipleChoice', 'text':'What is 2 * 2?',
       'subject':'Multiple Choice Subject',
       'choices':[{'text':'4', 'correct':True},
                  {'text':'2', 'correct':False},
                 {'text':'6', 'correct':False},
                 {'text':'8', 'correct':False}],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1, 'mctype': 'X'}
db.session.add(Question.from_dict(mcq))

mq = {'type':'Matching', 'text':'Pair the items',
      'subject':'Matching Subject',
      'texts':['Apples are', 'Bananas are',
               'Kiwis are', 'Pineapples are'],
      'answers':['Round', 'Long', 'Hairy', 'Spiky'],
      'hints': ['Hint1', 'Hint2'],
      'weight': 1}
db.session.add(Question.from_dict(mq))

rkq = {'type':'Ranking', 'text':'Rank these numbers',
       'subject':'Ranking Subject',
       'items':['1', '2', '3', '4'],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
db.session.add(Question.from_dict(rkq))

rkq = {'type':'Ranking', 'text':'Rank these numbers',
       'subject':'Ranking Subject',
       'items':['-2', '0', '2', '4'],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
db.session.add(Question.from_dict(rkq))

rkq = {'type':'Ranking', 'text':'Rank these numbers',
       'subject':'Ranking Subject',
       'items':['2', '4', '6', '8'],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
db.session.add(Question.from_dict(rkq))

db.session.commit()
