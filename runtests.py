from config import testdir
from unittest import TestLoader, TextTestRunner

ts = TestLoader().discover(testdir, '*.py')
TextTestRunner().run(ts)
