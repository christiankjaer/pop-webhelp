from flask import url_for, redirect, render_template, flash, abort, request, session
from .models import Threshold, Subject, Question, MultipleChoice, MCAnswer, TypeIn, Ranking, RankItem, Matching
from flask_login import login_required
from app import app, lm, db
from .forms import MultipleChoiceForm, TypeInForm
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

@app.route('/question/<string:name>')
def random_question(name):
    s = Subject.query.get(name)
    if not s.questions:
        return render_template('question/empty.html', subject=s)
    q = random.choice(s.questions)
    return redirect(url_for('view_question', id=q.id))

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
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

@app.route('/question/start/<string:subject>')
def start_answering(subject):
    qs = Question.query.filter_by(sub=subject).all()
    session['queue'] = [q.id for q in qs]
    return redirect(url_for('answer_question'))

@app.route('/question/answer', methods=['GET', 'POST'])
def answer_question():
    next_question = Question.query.get(session['queue'][-1])
    re = render_question(next_question)
    if re == True:
        session['queue'].pop()
        flash('Correct!, queue size = %s' % len(session['queue']))
        return redirect(url_for('answer_question'))
    elif re == False:
        session['queue'].insert(0, session['queue'].pop())
        flash('Correct!, queue size = %s' % len(session['queue']))
        return redirect(url_for('answer_question'))
    else: return re

@multimethod(MultipleChoice)
def render_question(q):
    form = MultipleChoiceForm()
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
    return render_template('question/multiplechoice.html', text=q.text, form=form)

@multimethod(TypeIn)
def render_question(q):
    form = TypeInForm()
    if form.validate_on_submit():
        if form.answer.data == q.answer:
            return True
        else:
            return False
    return render_template('question/typein.html', text=q.text, form=form)

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
    return render_template('question/ranking.html', text=q.text, items=items)

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
    return render_template('question/matching.html', text=q.text, items=items)

@app.template_filter()
def marktohtml(value):
    return markdown.markdown(value)
