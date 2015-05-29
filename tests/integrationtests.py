import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user
from app import app, db, lm
from app.user.models import User
from app.question.models import Threshold, Question, Subject
from app.user.token import generate_confirmation_token, confirm_token
from config import basedir
import unittest
from fillout_db import fillout

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        fillout()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_start_answer(self):
        rv = self.app.post('/login', data = dict(
            kuid='abc123',
            password='pwd'), follow_redirects=True)
        assert 'Subject' in rv.data
        assert 'abc123' in rv.data
        u = User.query.get('abc123')
        s = [t.subjects for t in Threshold.query.all() if t.is_open(u)][0]
        sub = s[0]
        rv = self.app.get('/subject/' + sub.name)
        assert sub.text in rv.data
        rv = self.app.get('/subject/start/'+str(sub.id), follow_redirects=True)
        q = sub.questions[0]
        assert q.text in rv.data

if __name__ == '__main__':
    unittest.main()
