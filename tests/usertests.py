import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user
from app import app, db, lm
from app.user.models import User
from app.user.token import generate_confirmation_token, confirm_token
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
        user = User('abc123', 'testpw', confirmed=True)
        db.session.add(user)
        db.session.commit()
        rv = self.app.post('/login', data = dict(
            kuid='abc123',
            password='testpw'), follow_redirects=True)

        assert 'Succesfully logged abc123 in' in rv.data

    def test_register(self):
        rv = self.app.post('/register', data = dict(
            kuid='abc123',
            password='testw',
            repeat_password='testw'), follow_redirects=True)
        user = User.query.get('abc123')
        assert user != None
        assert user.kuid == 'abc123'
        assert str(user) == '<User %s>' % user.kuid
        assert not user.is_anonymous()
        assert user.check_password('testw')

    def test_changepw(self):
        user = User('abc123', 'testpw', confirmed=True)
        db.session.add(user)
        db.session.commit()
        rv = self.app.post('/login', data = dict(
            kuid='abc123',
            password='testpw'), follow_redirects=True)
        rv = self.app.post('/changepw', data = dict(
            old_password = 'testpw',
            password = 'test2pw',
            repeat_password = 'test2pw'))
        user = User.query.get('abc123')
        assert user != None
        assert user.check_password('test2pw')

    def test_reset_pw(self):
        user = User('abc123', 'testpw', confirmed=True)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.kuid)
        rv = self.app.get('/reset/%s' % token, follow_redirects=True)
        user = User.query.get('abc123')
        assert user is not None
        assert not user.check_password('testpw')
        assert 'The new password has been sent' in rv.data

    def test_reset_pw_invalid(self):
        user = User('abc123', 'testpw', confirmed=True)
        db.session.add(user)
        db.session.commit()
        old_salt = app.config['SECURITY_PASSWORD_SALT']
        app.config['SECURITY_PASSWORD_SALT'] = 'something_else'
        token = generate_confirmation_token(user.kuid)
        app.config['SECURITY_PASSWORD_SALT'] = old_salt
        rv = self.app.get('/reset/%s' % token, follow_redirects=True)
        user = User.query.get('abc123')
        assert user is not None
        assert user.check_password('testpw')
        assert 'The confirmation link is invalid or has expired.' in rv.data

if __name__ == '__main__':
    unittest.main()
