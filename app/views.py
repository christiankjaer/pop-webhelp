from flask import redirect, url_for, render_template
from flask_login import login_required
from app import app

@app.route('/')
@login_required
def index():
    return redirect(url_for('overview'))
