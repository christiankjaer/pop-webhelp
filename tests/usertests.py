import os
from flask_sqlalchemy import SQLAlchemy
from app import app, db, lm
from app.models import User
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

    def test_add_user(self):
        user = User('abc123', 'testpw')
        db.session.add(user)
        db.session.commit()
        user = User.query.get('abc123')
        assert user != None
        assert user.kuid == 'abc123'
        assert user.check_password('testpw')

    def test_log_in(self):
        user = User('abc123', 'testpw')
        db.session.add(user)
        db.session.commit()
        rv = self.app.post('/login', data = dict(
            kuid='abc123',
            password='testpw'), follow_redirects=True)

        assert 'Succesfully logged abc123 in' in rv.data

    def test_register(self):
        rv = self.app.post('/register', data = dict(
            kuid='abc123',
            password='test',
            repeat_password='test'), follow_redirects=True)
        user = User.query.get('abc123')
        assert user != None
        assert user.kuid == 'abc123'
        assert user.check_password('test')


if __name__ == '__main__':
    unittest.main()
