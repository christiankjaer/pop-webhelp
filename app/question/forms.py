from flask_wtf import Form
from wtforms import SelectMultipleField, StringField, widgets, RadioField, TextAreaField
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultipleChoiceFormX(Form):
    choices = MultiCheckboxField('choices')
    def set_data(self, mc_question):
        self.choices.choices = map(lambda x: (str(x.id), x.text), mc_question.choices)

class MultipleChoiceForm1(Form):
    choices = RadioField('choices')
    def set_data(self, mc_question):
        self.choices.choices = map(lambda x: (str(x.id), x.text), mc_question.choices)

class TypeInForm(Form):
    answer = StringField('answer', validators=[DataRequired()])

class CodeForm(Form):
    codearea = TextAreaField()
