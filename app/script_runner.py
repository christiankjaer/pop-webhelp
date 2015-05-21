import subprocess
import json
import os
from config import basedir, scriptdir
def get_feedback(exec_name, answer):
    ex = os.path.join(basedir, scriptdir, exec_name)
    output = subprocess.check_output([ex, answer])
    return json.loads(output)
