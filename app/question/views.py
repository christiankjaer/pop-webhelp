from flask import url_for, redirect, render_template, flash, abort, request, session, jsonify
from .models import Threshold, Subject, Question, MultipleChoice, MCAnswer, TypeIn, Ranking, RankItem, Matching, Coding
from flask_login import login_required, current_user
from app import app, db
from .forms import MultipleChoiceForm1, MultipleChoiceFormX, TypeInForm, CodeForm
from multimethod import multimethod
from app.log.models import QLog, HintRating
from app.decorators import role_must_be
from app.script_runner import get_feedback
import random
import uuid

@app.route('/overview')
@login_required
def overview():
    thresholds = Threshold.make_list(current_user)
    if current_user.role == 'admin':
        for t in thresholds:
            t.open = True
    return render_template('question/overview.html', thresholds=thresholds)

@app.route('/subject/<string:name>')
@login_required
def view_subject(name):
    s = Subject.query.filter_by(name=name).first_or_404()
    if not s.threshold.is_open(current_user):
        return abort(403)
    if not s.questions:
        return render_template('question/empty.html', subject=s)
    return render_template('question/subject.html', subject=s)

@app.route('/subject/start/<int:sid>')
@login_required
def start_answering(sid):
    sub = Subject.query.get_or_404(sid)
    if not sub.threshold.is_open(current_user):
        return abort(403)
    session['session_id'] = str(uuid.uuid4())
    session['sid'] = sid
    session['uid'] = current_user.kuid
    session['score'] = 0
    session['goal'] = sub.goal
    session['queue'] = Subject.make_queue(sid)
    return redirect(url_for('answer_question'))

@app.route('/subject/question', methods=['GET', 'POST'])
@login_required
def answer_question():
    if not session.get('session_id', False):
        return abort(404)
    if session['score'] >= session['goal']:
        subject = Subject.query.get(session['sid'])
        if subject not in current_user.completed:
            current_user.completed.append(subject)
            db.session.add(current_user)
            db.session.commit()
        return render_template('question/finished.html')

    if len(session['queue']) == 0:
        session['queue'] = Subject.make_queue(session['sid'])

    session['qid'] = session['queue'][-1]
    session['correct'] = False
    question = Question.query.get(session['qid'])
    re = render_question(question)

    if request.method == 'POST' and type(re) == dict:
        log_entry = QLog(session, re)
        db.session.add(log_entry)
        db.session.commit()

        if re['correct']:
            session['score'] = session['score'] + question.weight
        else:
            session['queue'].insert(0, session['qid'])
        session['queue'].pop()
        return render_template('question/progress.html', feedback=re)
    
    else:
        session['hints'] = []
        return re

@role_must_be('admin')
@app.route('/question/<int:id>', methods=['GET', 'POST'])
@login_required
def view_question(id):
    session['hints'] = []
    q = Question.query.get_or_404(id)
    re = render_question(q)

    if request.method == 'POST':
        if re['correct']:
            flash('Perfect')
        else:
            flash('Wrong, try again')
        return redirect(url_for('view_question', id=q.id))

    return re

@multimethod(MultipleChoice)
def render_question(q):
    if q.mctype == '1':
        form = MultipleChoiceForm1()
    elif q.mctype == 'X':
        form = MultipleChoiceFormX()
    else:
        return abort(404)
    form.set_data(q)

    if form.validate_on_submit():
        answer = None
        if q.mctype == '1':
            answer = [form.choices.data]
        else:
            answer = form.choices.data

        correct = [c.id for c in q.choices if c.correct]
        feedback = 'The answer was correct.'
        result = {'answer': str(answer), 'correct':True, 'feedback':feedback}
        for i in answer:
            if int(i) not in correct:
                feedback = 'The answer was incorrect.'
                result['feedback'] = feedback
                result['correct'] = False
        return result

    random.shuffle(q.choices)
    return render_template('question/multiplechoice.html', 
                           text=q.text, form=form, qid=q.id)

@multimethod(TypeIn)
def render_question(q):
    form = TypeInForm()
    if form.validate_on_submit():
        answer = form.answer.data
        feedback = 'The answer was incorrect.'
        result = {'correct': False, 'answer': answer, 'feedback': feedback}
        if answer == q.answer:
            feedback = 'The answer was correct.'
            result['feedback'] = feedback
            result['correct'] = True
        return result

    return render_template('question/typein.html', 
                           text=q.text, form=form, qid=q.id)

@multimethod(Ranking)
def render_question(q):
    if request.method == 'POST':
        # The posted value is a comma seperated string like "1,3,4,6"
        answer = [int(x) for x in request.form['ranks'].split(',')]
        correct = [x.id for x in sorted(q.items, key=lambda y: y.rank)]
        # compare the id's
        feedback = 'The answer was incorrect.'
        result = {'correct': False, 'answer': str(answer), 'feedback': feedback}
        if answer == correct:
            feedback = 'The answer was correct.'
            result['feedback'] = feedback
            result['correct'] = True
        return result

    items = q.items
    random.shuffle(items)
    return render_template('question/ranking.html', 
                           text=q.text, items=items, qid=q.id)

@multimethod(Matching)
def render_question(q):
    if request.method == 'POST':
        answer = request.form['answers'].split(',')
        correct = [x.answer for x in q.items]
        feedback = 'The answer was incorrect.'
        result = {'correct': False, 'answer': str(answer), 'feedback': feedback}        
        if answer == correct:
            feedback = 'The answer was correct.'
            result['feedback'] = feedback
            result['correct'] = True
        return result

    texts = [x.text for x in q.items]
    answers = [x.answer for x in q.items]
    random.shuffle(answers)
    items = zip(texts, answers)
    return render_template('question/matching.html', 
                           text=q.text, items=items, qid=q.id)

@multimethod(Coding)
def render_question(q):
    form = CodeForm()
    form.codearea.data = q.code
    if form.validate_on_submit():
        answer = form.codearea.data
        feedback = get_feedback(q.exec_name, answer)
        feedback['answer'] = answer
        return feedback

    return render_template('question/coding.html', form = form, text=q.text, qid=q.id)

@app.route('/question/hint')
@login_required
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
@login_required
def rate_hint():
    hid = request.args.get('hid', 0, type=int)
    status = request.args.get('status', None)
    hr = HintRating(hid, status)
    db.session.add(hr)
    db.session.commit()
    return jsonify(status='Rating sent')


