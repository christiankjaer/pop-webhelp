import os
from flask_sqlalchemy import SQLAlchemy
from app import app, db, lm
from app.user.models import User
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
        user = User('wkm839', 'testpw')
        db.session.add(user)
        db.session.commit()
        user = User.query.get('wkm839')
        assert user != None
        assert user.kuid == 'wkm839'
        assert user.check_password('testpw')

    def test_log_in(self):
        user = User('wkm839', 'testpw', confirmed=True)
        db.session.add(user)
        db.session.commit()
        rv = self.app.post('/login', data = dict(
            kuid='wkm839',
            password='testpw'), follow_redirects=True)

        assert 'Succesfully logged wkm839 in' in rv.data

    def test_register(self):
        rv = self.app.post('/register', data = dict(
            kuid='wkm839',
            password='testw',
            repeat_password='testw'), follow_redirects=True)
        user = User.query.get('wkm839')
        assert user != None
        assert user.kuid == 'wkm839'
        assert user.check_password('testw')


if __name__ == '__main__':
    unittest.main()
