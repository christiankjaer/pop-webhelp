import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user
from app import app, db, lm
from app.question.models import TypeIn, Question, MultipleChoice, Subject, Threshold
from config import basedir
import unittest

class UserTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_from_dict_typein(self):
        t = Threshold('T1')
        s = Subject('S1', 'Subject1', t)
        d = {'type': 'TypeIn', 'subject':'S1', 'text': 'Text1', 'answer': 'Answer1'}
        q = Question.from_dict(d)
        assert type(q) == TypeIn
        assert q.text == 'Text1'
        assert q.answer == 'Answer1'


    def test_from_dict_mc(self):
        t = Threshold('T1')
        s = Subject('S1', 'Subject1', t)
        d = {
            'type': 'MultipleChoice',
            'subject': 'S1',
            'text': 'Text2',
            'answer': [{
                'text': 'Answer1',
                'correct': True}, {
                'text': 'Answer2',
                'correct': False}]
        }
        q = Question.from_dict(d)
        assert type(q) == MultipleChoice
        assert q.text == 'Text2'
        assert len(q.choices) == 2
        assert q.choices[0].text == 'Answer1'
        assert q.choices[0].correct
        assert q.choices[1].text == 'Answer2'
        assert not q.choices[1].correct

if __name__ == '__main__':
    unittest.main
