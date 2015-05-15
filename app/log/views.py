from flask import url_for, redirect, render_template, flash, abort, request
from .models import QLog
from app import app, lm, db

@app.route('/log')
def log_overview():
    log_entries = QLog.query.all()
    return render_template('log/log.html', log_entries=log_entries)
