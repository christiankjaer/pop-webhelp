from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import request, flash, redirect, url_for
from flask_login import current_user
from werkzeug import secure_filename
import yaml
from app.decorators import role_must_be

from app import app, adm, db
from app.question.models import Question, Subject, Threshold, TypeIn, MultipleChoice, MCAnswer, Ranking, RankItem, Matching, MatchItem, Hint, Coding

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.role == 'admin'

class AdminView(BaseView):
    @expose('/')
    def admin_index(self):
        return self.render('admin/index.html')

class ToOverview(BaseView):
    @expose('/')
    def to_overview(self):
        return redirect(url_for('overview'))

class FileUpload(BaseView):
    def is_accessible(self):
        return current_user.role == 'admin'
    @expose('/', methods=['GET', 'POST'])
    def upload_file(self):
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                read_yaml(file)
                flash('File succesfully uploaded')
            else:
                flash('Invalid file type.')
        return self.render('admin/upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def read_yaml(file):
    data = yaml.load(file)
    if data.get('subject', None):
        obj = Question.from_dict(data)
    elif data.get('threshold', None):
        obj = Subject.from_dict(data)
    elif data.get('name', None):
        obj = Threshold.from_dict(data)
    else:
        obj = None

    if not obj:
        flash('Invalid File Format')
    else:
        db.session.add(obj)
        db.session.commit()

class ThresholdView(AdminModelView):
    column_list = ('id', 'name', 'goal', 'next')
    column_sortable_list = ('id', 'name', 'next')

class SubjectView(AdminModelView):
    column_list = ('id', 'name', 'text', 'goal', 'threshold')
    column_sortable_list = ('id', 'name', 'threshold')

class TypeInView(AdminModelView):
    column_list = ('id', 'text', 'answer', 'weight', 'subject')
    column_sortable_list = ('id', 'subject')

class MultipleChoiceView(AdminModelView):
    column_list = ('id', 'text', 'weight', 'mctype', 'subject')
    column_sortable_list = ('id', 'mctype', 'subject')

class MCAnswerView(AdminModelView):
    column_list = ('mcid', 'text', 'correct')
    column_labels = dict(mcid='Multiple Choice Question ID')
    column_sortable_list = (('mcid', MCAnswer.mcid))

class RankingView(AdminModelView):
    column_list = ('id', 'text', 'weight', 'subject')
    column_sortable_list = ('id', 'subject')

class RankItemView(AdminModelView):
    column_list = ('rid', 'text', 'rank')
    column_labels = dict(rid='Ranking Question ID')
    column_sortable_list = (('rid', RankItem.rid))

class MatchingView(AdminModelView):
    column_list = ('id', 'text', 'weight', 'subject')
    column_sortable_list = ('id', 'subject')

class MatchItemView(AdminModelView):
    column_list = ('mid', 'text', 'answer')
    column_labels = dict(mid='Matching Question ID')
    column_sortable_list = (('mid', MatchItem.mid))

class CodingView(AdminModelView):
    column_list = ('id', 'text', 'weight', 'code', 'exec_name')
    column_sortable_list = ('id', 'subject')

class HintView(AdminModelView):
    column_list = ('qid', 'text')
    column_labels = dict(qid='Question ID')
    column_sortable_list = (('qid', Hint.qid))

adm.add_view(ToOverview(name='Overview'))
adm.add_view(FileUpload(name='Upload File'))
adm.add_view(ThresholdView(Threshold, db.session))
adm.add_view(SubjectView(Subject, db.session))
adm.add_view(AdminModelView(Question, db.session, name='Question', category='Questions'))
adm.add_view(TypeInView(TypeIn, db.session, name='Type In', category='Questions'))
adm.add_view(CodingView(Coding, db.session, name='Coding', category='Questions'))
adm.add_view(MultipleChoiceView(MultipleChoice, db.session, name='Multiple Choice', category='Questions'))
adm.add_view(MCAnswerView(MCAnswer, db.session, name='Multiple Choice Answer', category='Questions'))
adm.add_view(RankingView(Ranking, db.session, name='Ranking', category='Questions'))
adm.add_view(RankItemView(RankItem, db.session, name='Ranking Items', category='Questions'))
adm.add_view(MatchingView(Matching, db.session, name='Matching', category='Questions'))
adm.add_view(MatchItemView(MatchItem, db.session, name='Matching Item', category='Questions'))
adm.add_view(HintView(Hint, db.session, name='Hint', category='Questions'))
