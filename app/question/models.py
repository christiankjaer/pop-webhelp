from app import db

class Threshold(db.Model):
    __tablename__ = 'threshold'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    next = db.Column(db.Integer, db.ForeignKey('threshold.id'), default=None)
    subjects = db.relationship('Subject', backref='threshold')

    def __init__(self, name, next=None):
        self.name = name
        self.next = next

    def __repr__(self):
        return 'Threshold %s' % (self.id)

class Subject(db.Model):
    __tablename__ = 'subject'
    name = db.Column(db.String(50), primary_key=True)
    text = db.Column(db.Text())
    thres = db.Column(db.Integer, db.ForeignKey('threshold.id'))
    questions = db.relationship('Question', backref='subject')
    
    def __init__(self, name, text, thres):
        self.name = name
        self.text = text
        self.thres = thres

    def __repr__(self):
        return 'Subject %s' % (self.name)

class Question(db.Model):
    """ This is the Question base class """
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    text = db.Column(db.Text())
    sub = db.Column(db.String(50), db.ForeignKey('subject.name'))

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
            q.sub = data['subject']
            for answer in data['answer']:
                a = MCAnswer()
                a.text = answer['text']
                a.correct = answer['correct']
                q.choices.append(a)
        elif data['type'] == 'TypeIn':
            q = TypeIn()
            q.text = data['text']
            q.sub = data['subject']
            q.answer = data['answer']
        elif data['type'] == 'Ranking':
            q = Ranking()
            q.text = data['text']
            q.sub = data['subject']
            for i, item in enumerate(data['items']):
                ri = RankItem()
                ri.rank = i
                ri.text = item
                q.items.append(ri)
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
    choices = db.relationship('MCAnswer', backref='multiple_choice')

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

class Ranking(Question):
    __tablename__ = 'ranking'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    items = db.relationship('RankItem', backref='ranking')

    __mapper_args__ = {
        'polymorphic_identity':'ranking'
    }

    def __repr__(self):
        return 'Ranking Question %s' % (self.id)

class RankItem(db.Model):
    __tablename__ = 'rank_item'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    rank = db.Column(db.Integer)
    rid = db.Column(db.Integer, db.ForeignKey('ranking.id'))

    def __repr__(self):
        return 'Ranking Item %s' % (self.id)
