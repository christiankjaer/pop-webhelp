from flask import url_for, redirect, render_template, flash, abort, request
from .models import QLog
from app import app, lm, db
from app.decorators import role_must_be

@app.route('/log')
@role_must_be('admin')
def log_overview():
    log_entries = QLog.query.all()
    return render_template('log/log.html', log_entries=log_entries)
