from flask import url_for, redirect, render_template, flash
from .models import Question, MultipleChoice, MCAnswer
from app import app, lm, db
from .forms import MultipleChoiceForm

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
    q = Question.query.get(id)
    form = MultipleChoiceForm()
    form.choices.choices = map(lambda x: (str(x.id), x.text), q.choices)

    if form.validate_on_submit():
        correct = map(lambda c: c.id, filter(lambda c: c.correct, q.choices))
        print correct
        if len(correct) != len(form.choices.data):
            return "fail"
        for i in form.choices.data:
            print int(i)
            if int(i) not in correct:
                return "fail"
        return "success"
    return render_template('question/multiplechoice.html', text = q.text, form=form)
