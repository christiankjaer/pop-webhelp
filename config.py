import os
basedir = os.path.abspath(os.path.dirname(__file__))
testdir = 'tests'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SECURITY_PASSWORD_SALT = 'pass-the-salt'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# gmail authentication
if 'APP_MAIL_USERNAME' in os.environ:
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
else:
    MAIL_USERNAME = None

if 'APP_MAIL_PASSWORD' in os.environ:
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
else:
    MAIL_PASSWORD = None

# mail accounts
MAIL_DEFAULT_SENDER = 'from@example.com'

# App specific settings
USER_EMAIL_SUFFIX = '@alumni.ku.dk'
TESTING = False
