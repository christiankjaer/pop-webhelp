from app import db
from app.user.models import User
from app.question.models import *

user = User('abc123', 'pwd', confirmed=True, role='student')
db.session.add(user)

user = User('def456', 'test', confirmed=True, role='admin')
db.session.add(user)

thres = {'name':'Modules'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Polymorphism', 'next':'Modules'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Higher order functions', 'next':'Polymorphism'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Control Structures', 'next':'Higher order functions'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Types', 'next':'Control Structures'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Functions', 'next':'Types'}
db.session.add(Threshold.from_dict(thres))

thres = {'name':'Basics', 'next':'Functions'}
db.session.add(Threshold.from_dict(thres))

sub = {'name':'Integers and reals', 'text':'This subject is about the basic number types in F#',
      'threshold':'Basics', 'goal':10}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Expressions', 'text':'Everything in functional programming is expressions',
       'threshold':'Basics', 'goal':10}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Strings', 'text':'It is useful to be able to manipulate strings in programming',
       'threshold':'Basics', 'goal':8}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Truth values', 'text':'This makes it possible to make decisions',
       'threshold':'Basics', 'goal':10}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Arguments', 'text':'Functions have arguments',
       'threshold':'Functions', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Pattern matching', 'text':'Important stuff',
       'threshold':'Functions', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Recursion', 'text':'Important stuff',
       'threshold':'Functions', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Tuples', 'text':'Important stuff',
       'threshold':'Types', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Lists', 'text':'Important stuff',
       'threshold':'Types', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'Simple datatypes', 'text':'Important stuff',
       'threshold':'Types', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'if-then-else expressions', 'text':'Important stuff',
       'threshold':'Control Structures', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'case expressions', 'text':'Important stuff',
       'threshold':'Control Structures', 'goal':5}
db.session.add(Subject.from_dict(sub))

sub = {'name':'let-statements', 'text':'Important stuff',
       'threshold':'Control Structures', 'goal':5}
db.session.add(Subject.from_dict(sub))

db.session.commit()
