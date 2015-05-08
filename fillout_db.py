from app import db
from app.user.models import User
from app.question.models import *

data = []

user = User('abc123', 'pwd', confirmed=True)
data += [user]

t1 = Threshold('TypeIn Threshold', 4)
t2 = Threshold('Multiple Choice Threshold', 3)
t3 = Threshold('Ranking Threshold', 2)
t4 = Threshold('Empty Threshold', 5)
t5 = Threshold('Matching Threshold')
data += [t1, t4, t3, t2, t5]

s1 = Subject('TypeIn Subject', 'This is Test Subject 1', 1, goal=4)
s2 = Subject('Multiple Choice Subject', 'This is Test Subject 2', 4, goal=2)
s3 = Subject('Ranking Subject', 'This is Test Subject 3', 3, goal=2)
s4 = Subject('Empty Subject', 'This is Test Subject 4', 2, goal=2)
s5 = Subject('Matching Subject', 'This is Test Subject 5', 5, goal=2)
data += [s1, s2, s3, s4, s5]

tiq = {'type':'TypeIn', 'text':'What is 2 + 2?', 'subject':'TypeIn Subject',
       'answer':'4',
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(tiq)]

tiq = {'type':'TypeIn', 'text':'What is 2 - 2?', 'subject':'TypeIn Subject',
       'answer':'0',
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(tiq)]

tiq = {'type':'TypeIn', 'text':'What is 2 * 2?', 'subject':'TypeIn Subject',
       'answer':'4',
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(tiq)]

tiq = {'type':'TypeIn', 'text':'What is 2 / 2?', 'subject':'TypeIn Subject',
       'answer':'1',
       'hints': ['Hint1', 'Hint2'],
       'weight': 2}
data += [Question.from_dict(tiq)]

mcq = {'type':'MultipleChoice', 'text':'What is 2 + 2?',
       'subject':'Multiple Choice Subject',
       'answer':[{'text':'3', 'correct':False},
                 {'text':'4', 'correct':True},
                 {'text':'5', 'correct':False},
                 {'text':'6', 'correct':False}],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1, 'mctype': '1'}
data += [Question.from_dict(mcq)]

mcq = {'type':'MultipleChoice', 'text':'What is 2 - 2?',
       'subject':'Multiple Choice Subject',
       'answer':[{'text':'-2', 'correct':False},
                 {'text':'0', 'correct':True},
                 {'text':'2', 'correct':False},
                 {'text':'4', 'correct':False}],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1, 'mctype': 'X'}
data += [Question.from_dict(mcq)]

mcq = {'type':'MultipleChoice', 'text':'What is 2 * 2?',
       'subject':'Multiple Choice Subject',
       'answer':[{'text':'2', 'correct':False},
                 {'text':'4', 'correct':True},
                 {'text':'6', 'correct':False},
                 {'text':'8', 'correct':False}],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1, 'mctype': 'X'}
data += [Question.from_dict(mcq)]

mq = {'type':'Matching', 'text':'Pair the items',
        'subject':'Matching Subject',
        'items': [
            ('Apples are', 'Round'),
            ('Bananas are', 'Long'),
            ('Kiwis are', 'Hairy'),
            ('Pineapples are', 'Spiky')],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(mq)]

rkq = {'type':'Ranking', 'text':'Rank these numbers',
       'subject':'Ranking Subject',
       'items':['1', '2', '3', '4'],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(rkq)]

rkq = {'type':'Ranking', 'text':'Rank these numbers',
       'subject':'Ranking Subject',
       'items':['-2', '0', '2', '4'],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(rkq)]

rkq = {'type':'Ranking', 'text':'Rank these numbers',
       'subject':'Ranking Subject',
       'items':['2', '4', '6', '8'],
       'hints': ['Hint1', 'Hint2'],
       'weight': 1}
data += [Question.from_dict(rkq)]

for d in data:
    db.session.add(d)
db.session.commit()

