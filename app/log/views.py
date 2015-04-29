from flask import url_for, redirect, render_template, flash, abort, request
from .models import QLog, Session
from app import app, lm, db
import markdown
