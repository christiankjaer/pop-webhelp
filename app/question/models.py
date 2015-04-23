from app import db

class Question(db.Model):
    """ This is the Question base class """
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    text = db.Column(db.Text())

    __mapper_args__ = {
        'polymorphic_identity':'question',
        'polymorphic_on':type
    }

    def __repr__(self):
        return 'Question %s' % (self.id)

    @staticmethod
    def from_dict(data):
        q = None
        if data['type'] == 'MultipleChoice':
            q = MultipleChoice()
            q.text = data['text']
            for answer in data['answer']:
                a = MCAnswer()
                a.text = answer['text']
                a.correct = answer['correct']
                q.choices.append(a)
        elif data['type'] == 'TypeIn':
            q = TypeIn()
            q.text = data['text']
            q.answer = data['answer']
        return q

class TypeIn(Question):
    __tablename__ = 'type_in'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    answer = db.Column(db.String(255))
    __mapper_args__ = {
        'polymorphic_identity':'type_in'
    }

    def __repr__(self):
        return 'Type In Question %s' % self.id

class MultipleChoice(Question):
    """ This is the multiple choice question class """
    __tablename__ = 'multiple_choice'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    choices = db.relationship('MCAnswer', backref='question')

    __mapper_args__ = {
        'polymorphic_identity':'multiple_choice'
    }

    def __repr__(self):
        return 'Multiple Choice Question %s' % (self.id)

class MCAnswer(db.Model):
    """ This is the multiple choice answer class """
    __tablename__ = 'mcanswer'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    correct = db.Column(db.Boolean())
    mcid = db.Column(db.Integer, db.ForeignKey('multiple_choice.id'))

    def __repr__(self):
        return 'Multiple Choice Answer %s' % (self.id)

