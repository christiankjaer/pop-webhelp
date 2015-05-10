from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import request, flash
from werkzeug import secure_filename
import yaml

from app import app, adm, db
from app.question.models import Question, Subject, Threshold, TypeIn, MultipleChoice, MCAnswer, Ranking, RankItem, Matching, MatchItem, Hint

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class FileUpload(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def upload_file(self):
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                #filename = secure_filename(file.filename)
                read_yaml(file)
                #data = yaml.load(file)
                #p = Post(data['title'], data['text'])
                #db.session.add(p)
                #db.session.commit()
                flash('File succesfully uploaded')
                return self.render('admin/upload.html')
            else:
                flash('Invalid file type.')
                return self.render('admin/upload.html')
        return self.render('admin/upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def read_yaml(file):
    pass

adm.add_view(FileUpload(name='Upload File'))
adm.add_view(ModelView(Threshold, db.session))
adm.add_view(ModelView(Subject, db.session))
adm.add_view(ModelView(Question, db.session, name='Question', category='Questions'))
adm.add_view(ModelView(TypeIn, db.session, name='Type In', category='Questions'))
adm.add_view(ModelView(MultipleChoice, db.session, name='Multiple Choice', category='Questions'))
adm.add_view(ModelView(MCAnswer, db.session, name='Multiple Choice Answer', category='Questions'))
adm.add_view(ModelView(Ranking, db.session, name='Ranking', category='Questions'))
adm.add_view(ModelView(RankItem, db.session, name='Ranking Items', category='Questions'))
adm.add_view(ModelView(Matching, db.session, name='Matching', category='Questions'))
adm.add_view(ModelView(MatchItem, db.session, name='Matching Item', category='Questions'))
adm.add_view(ModelView(Hint, db.session, name='Hint', category='Questions'))
