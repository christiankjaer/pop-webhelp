from flask import url_for, redirect, render_template, flash, abort
from .models import Question, MultipleChoice, MCAnswer, TypeIn, Ranking
from app import app, lm, db
from .forms import MultipleChoiceForm, TypeInForm

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
    q = Question.query.get(id)
    if q is None:
        return abort(404)
    elif type(q) == MultipleChoice:
        form = MultipleChoiceForm()
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

    elif type(q) == TypeIn:
        form = TypeInForm()
        if form.validate_on_submit():
            if form.answer.data == q.answer:
                return "success"
            else:
                return "fail"
        return render_template('question/typein.html', text=q.text, form=form)
    elif type(q) == Ranking:
        return render_template('question/ranking.html', q=q)


