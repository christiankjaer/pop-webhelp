from flask import url_for, redirect, render_template, flash, abort, request, session, jsonify
from .models import Threshold, Subject, Question, MultipleChoice, MCAnswer, TypeIn, Ranking, RankItem, Matching
from flask_login import login_required, current_user
from app import app, lm, db
from .forms import MultipleChoiceForm1, MultipleChoiceFormX, TypeInForm
import random
from multimethod import multimethod
import uuid
from app.log.models import QLog
from flask_sqlalchemy import get_debug_queries

@app.route('/overview')
@login_required
def overview():
    thresholds = []
    subquery = db.session.query(Threshold.next).filter(Threshold.next != None)
    t = db.session.query(Threshold).filter(~Threshold.id.in_(subquery)).first()
    t.open = False
    thresholds.append(t)
    while t and t.next != None:
        t = Threshold.query.get(t.next)
        t.open = False
        thresholds.append(t)
    for threshold in thresholds:
        threshold.open = True
        if not all([s in current_user.completed for s in threshold.subjects]):
            break

    return render_template('question/overview.html', thresholds=thresholds)

@app.route('/subject/<string:name>')
def view_subject(name):
    s = Subject.query.filter_by(name=name).first()
    if not s.questions:
        return render_template('question/empty.html', subject=s)
    return render_template('question/subject.html', subject=s)

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
    session['hints'] = []
    q = Question.query.get(id)
    if not q:
        return abort(404)
    re = render_question(q)
    if request.method == 'POST' and type(re) == dict:
        if re['correct']:
            flash('Perfect')
            return redirect(url_for('overview'))
        else:
            flash('Wrong, try again')
            return redirect(url_for('view_question', id=q.id))
    else: return re

@app.route('/subject/start/<int:sid>')
def start_answering(sid):
    sub = Subject.query.get_or_404(sid)
    qs = Question.query.filter_by(sub=sub.id).all()
    session['sid'] = sid
    session['score'] = 0
    session['goal'] = sub.goal
    session['queue'] = make_queue(sid)
    session['session_id'] = str(uuid.uuid4())
    return redirect(url_for('answer_question'))

def make_queue(sid):
    qs = Question.query.filter_by(sub=sid).all()
    return [q.id for q in qs]

@app.route('/subject/question', methods=['GET', 'POST'])
def answer_question():
    if session['score'] >= session['goal']:
        subject = Subject.query.get(session['sid'])
        if subject not in current_user.completed:
            current_user.completed.append(subject)
            db.session.add(current_user)
            db.session.commit()
        return render_template('question/finished.html')

    if len(session['queue']) == 0:
        session['queue'] = make_queue(session['sid'])

    question = Question.query.get(session['queue'][-1])
    re = render_question(question)

    if request.method == 'POST' and type(re) == dict:
        # Ugly hack, but shuffling the choices of the questions makes SQLAlchemy go crazy
        db.session.rollback()
        log_entry = QLog(question.id, current_user.kuid, session['session_id'], re['answer'], re['correct'], len(session['hints']))
        db.session.add(log_entry)
        db.session.commit()
        if re['correct']:
            session['score'] = session['score'] + question.weight
            session['queue'].pop()
            return render_template('question/progress.html', feedback=re)
        else:
            session['queue'].insert(0, session['queue'].pop())
            return render_template('question/progress.html', feedback=re)
    else:
        session['hints'] = []
        return re

@multimethod(MultipleChoice)
def render_question(q):
    if q.mctype == '1':
        form = MultipleChoiceForm1()
    elif q.mctype == 'X':
        form = MultipleChoiceFormX()
    else:
        return abort(404)
    random.shuffle(q.choices)
    form.set_data(q)
    if form.validate_on_submit():
        answer = None
        if q.mctype == '1':
            answer = [form.choices.data]
        else:
            answer = form.choices.data
        correct = [c.id for c in q.choices if c.correct]
        if len(correct) != len(answer):
            return {'correct': False, 'feedback': 'The answer was incorrect', 'answer': str(answer)}
        for i in answer:
            if int(i) not in correct:
                return {'correct': False, 'feedback': 'The answer was incorrect' , 'answer': str(answer)}
        return {'correct': True, 'feedback': 'The answer was correct', 'answer': str(answer)}
    return render_template('question/multiplechoice.html', text=q.text, form=form, qid=q.id)

@multimethod(TypeIn)
def render_question(q):
    form = TypeInForm()
    if form.validate_on_submit():
        if form.answer.data == q.answer:
            return {'correct': True, 'feedback': 'The answer was correct', 'answer': q.answer}
        else:
            return {'correct': False, 'feedback': 'The answer was incorrect', 'answer': q.answer}
    return render_template('question/typein.html', text=q.text, form=form, qid=q.id)

@multimethod(Ranking)
def render_question(q):
    if request.method == 'POST':
        # The posted value is a comma seperated string like "1,3,4,6"
        answer = [int(x) for x in request.form['ranks'].split(',')]
        correct = [x.id for x in sorted(q.items, key=lambda y: y.rank)]
        # compare the id's
        if answer == correct:
            return {'correct': True, 'feedback': 'The answer was correct', 'answer': str(answer)}
        else:
            return {'correct': False, 'feedback': 'The answer was incorrect', 'answer': str(answer)}
    items = q.items
    random.shuffle(items)
    return render_template('question/ranking.html', text=q.text, items=items, qid=q.id)

@multimethod(Matching)
def render_question(q):
    if request.method == 'POST':
        answer = request.form['answers'].split(',')
        correct = [x.answer for x in q.items]
        if answer == correct:
            return {'correct': True, 'feedback': 'The answer was correct', 'answer': str(answer)}
        else:
            return {'correct': False, 'feedback': 'The answer was incorrect', 'answer': str(answer)}
    texts = [x.text for x in q.items]
    answers = [x.answer for x in q.items]
    random.shuffle(answers)
    items = zip(texts, answers)
    return render_template('question/matching.html', text=q.text, items=items, qid=q.id)

@app.route('/question/hint')
def get_hint():
    qid = request.args.get('qid', 0, type=int)
    hints = Question.query.get_or_404(qid).hints
    # We assume that the already given hints are stored in the session cookie
    old_hints = session.get('hints', [])
    new_hints = [h for h in hints if h.id not in old_hints]
    if len(new_hints) > 0:
        session.setdefault('hints', [])
        h = new_hints[0]
        session['hints'].append(h.id)
        return jsonify(hint=h.text, id=h.id)
    else:
        return abort(404)

@app.route('/question/hint/rate')
def rate_hint():
    hid = request.args.get('hid', 0, type=int)
    status = request.args.get('status', None)
    return jsonify(status="%s - %s" % (status, hid))
