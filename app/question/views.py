from flask import url_for, redirect, render_template, flash, abort, request, session, jsonify
from .models import Threshold, Subject, Question, MultipleChoice, MCAnswer, TypeIn, Ranking, RankItem, Matching
from flask_login import login_required
from app import app, lm, db
from .forms import MultipleChoiceForm1, MultipleChoiceFormX, TypeInForm
import random
import markdown
from multimethod import multimethod

@app.route('/overview')
@login_required
def overview():
    thresholds = []
    subquery = db.session.query(Threshold.next).filter(Threshold.next != None)
    t = db.session.query(Threshold).filter(~Threshold.id.in_(subquery)).first()
    thresholds.append(t)
    while t and t.next != None:
        t = Threshold.query.get(t.next)
        thresholds.append(t)
    return render_template('question/overview.html', thresholds=thresholds)

@app.route('/subject/<string:name>')
def random_question(name):
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
    if re == True:
        flash('Perfect')
        return redirect(url_for('overview'))
    elif re == False:
        flash('Wrong, try again')
        return redirect(url_for('view_question', id=q.id))
    else: return re

@app.route('/subject/start/<int:sid>')
def start_answering(sid):
    sub = Subject.query.get_or_404(sid)
    qs = Question.query.filter_by(sub=sub.name).all()
    session['score'] = 0
    session['goal'] = sub.goal
    session['queue'] = [q.id for q in qs]
    return redirect(url_for('answer_question'))

@app.route('/question/answer', methods=['GET', 'POST'])
def answer_question():
    if session['score'] >= session['goal']:
        return render_template('question/finished.html')
    next_question = Question.query.get(session['queue'][-1])
    re = render_question(next_question)
    if re == True:
        session['score'] = session['score'] + next_question.weight
        session['queue'].pop()
        return render_template('question/progress.html', feedback='RIGTIGT')
    elif re == False:
        session['queue'].insert(0, session['queue'].pop())
        return render_template('question/progress.html', feedback='FORKERT')
    else: return re

@multimethod(MultipleChoice)
def render_question(q):
    if q.mctype == '1':
        form = MultipleChoiceForm1()
    elif q.mctype == 'X':
        form = MultipleChoiceFormX()
    else:
        print 'Multiple Choice Type Missing!'
        return abort(404)
    random.shuffle(q.choices)
    form.set_data(q)
    if form.validate_on_submit():
        correct = [c.id for c in q.choices if c.correct]
        if len(correct) != len(form.choices.data):
            return False
        for i in form.choices.data:
            if int(i) not in correct:
                return False
        return True
    return render_template('question/multiplechoice.html', text=q.text, form=form, qid=q.id)

@multimethod(TypeIn)
def render_question(q):
    form = TypeInForm()
    if form.validate_on_submit():
        if form.answer.data == q.answer:
            return True
        else:
            return False
    return render_template('question/typein.html', text=q.text, form=form, qid=q.id)

@multimethod(Ranking)
def render_question(q):
    if request.method == 'POST':
        # The posted value is a comma seperated string like "1,3,4,6"
        answer = [int(x) for x in request.form['ranks'].split(',')]
        correct = [x.id for x in sorted(q.items, key=lambda y: y.rank)]
        # compare the id's
        if answer == correct:
            return True
        else:
            return False
    items = q.items
    random.shuffle(items)
    return render_template('question/ranking.html', text=q.text, items=items, qid=q.id)

@multimethod(Matching)
def render_question(q):
    if request.method == 'POST':
        answer = request.form['answers'].split(',')
        correct = [x.answer for x in q.items]
        if answer == correct:
            return True
        else:
            return False
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

@app.template_filter()
def marktohtml(value):
    return markdown.markdown(value)
