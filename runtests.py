from config import testdir, basedir
from unittest import TestLoader, TextTestRunner
from coverage import coverage
import os

cov = coverage(branch=True,
        omit=['bin/*', 'lib/*', 'tests/*', 'include/*', 'doc/*', '/usr/*'])
cov.start()
ts = TestLoader().discover(testdir, '*.py')
TextTestRunner().run(ts)
cov.stop()
cov.save()
print "\n\nCoverage Report:\n"
cov.report()
print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
cov.html_report(directory='tmp/coverage')
cov.erase()
