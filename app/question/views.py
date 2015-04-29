from flask import url_for, redirect, render_template, flash, abort, request
from .models import Threshold, Subject, Question, MultipleChoice, MCAnswer, TypeIn, Ranking, RankItem, Matching
from flask_login import login_required
from app import app, lm, db
from .forms import MultipleChoiceForm, TypeInForm
import random
import markdown

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
    elif type(q) == MultipleChoice:
        return render_multiple_choice(q)
    elif type(q) == TypeIn:
        return render_type_in(q)
    elif type(q) == Ranking:
        return render_ranking(q)
    elif type(q) == Matching:
        return render_matching(q)

def render_multiple_choice(q):
    form = MultipleChoiceForm()
    random.shuffle(q.choices)
    form.set_data(q)
    if form.validate_on_submit():
        correct = map(lambda c: c.id, filter(lambda c: c.correct, q.choices))
        if len(correct) != len(form.choices.data):
            return "fail"
        for i in form.choices.data:
            if int(i) not in correct:
                return "fail"
        return "success"
    return render_template('question/multiplechoice.html', text=q.text, form=form)

def render_type_in(q):
    form = TypeInForm()
    if form.validate_on_submit():
        if form.answer.data == q.answer:
            return "success"
        else:
            return "fail"
    return render_template('question/typein.html', text=q.text, form=form)

def render_ranking(q):
    if request.method == 'POST':
        # The posted value is a comma seperated string like "1,3,4,6"
        answer = map(lambda x: int(x), request.form['ranks'].split(','))
        correct = map(lambda x: x.id, sorted(q.items, key=lambda y: y.rank))
        # compare the id's
        if answer == correct:
            return "success"
        else:
            return "fail"
    items = q.items
    random.shuffle(items)
    return render_template('question/ranking.html', text=q.text, items=items)

def render_matching(q):
    if request.method == 'POST':
        answer = request.form['answers'].split(',')
        correct = map(lambda x: x.answer, q.items)
        if answer == correct:
            return "success"
        else:
            return "fail"
    texts = map(lambda x: x.text, q.items)
    answers = map(lambda x: x.answer, q.items)
    random.shuffle(answers)
    items = zip(texts, answers)
    return render_template('question/matching.html', text=q.text, items=items)

@app.template_filter()
def marktohtml(value):
    return markdown.markdown(value)
