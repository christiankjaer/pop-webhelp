from flask_admin import Admin, BaseView, expose
from flask_admin.contrib import sqla

from app import adm, db
from app.question.models import Question, Subject, Threshold

adm.add_view(sqla.ModelView(Subject, db.session))
adm.add_view(sqla.ModelView(Threshold, db.session))
adm.add_view(sqla.ModelView(Question, db.session))
