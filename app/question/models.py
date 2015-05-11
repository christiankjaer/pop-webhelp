from app import db

class Threshold(db.Model):
    __tablename__ = 'threshold'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    goal = db.Column(db.Integer)
    next = db.Column(db.Integer, db.ForeignKey('threshold.id'), default=None)
    subjects = db.relationship('Subject', backref='threshold')

    def __init__(self, name, next=None, goal=0):
        self.name = name
        self.next = next
        self.goal = goal

    def __repr__(self):
        return 'Threshold %s' % (self.id)

    @staticmethod
    def from_dict(data):
        return Threshold(data['Name'], data['next'], data['goal'])

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text())
    goal = db.Column(db.Integer)
    thres = db.Column(db.Integer, db.ForeignKey('threshold.id'))
    questions = db.relationship('Question', backref='subject')

    def __init__(self, name, text, thres, goal):
        self.name = name
        self.text = text
        self.thres = thres
        self.goal = goal

    def __repr__(self):
        return 'Subject %s' % (self.name)

    @staticmethod
    def from_dict(data):
        return Subject(data['name'], data['text'], data['thres'], data['goal'])

class Question(db.Model):
    """ This is the Question base class """
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    text = db.Column(db.Text())
    weight = db.Column(db.Integer, default=0)
    sub = db.Column(db.String(50), db.ForeignKey('subject.name'))
    hints = db.relationship('Hint', backref='question')

    __mapper_args__ = {
        'polymorphic_identity':'question',
        'polymorphic_on':type
    }

    def __repr__(self):
        return 'Question %s' % (self.id)

    @staticmethod
    def from_dict(data):
        if 'qtype' in data:
            qtype = data['qtype']
        else:
            return None

        if qtype == 'MultipleChoice' and 'answer' in data and 'mctype' in data:
            q = MultipleChoice(data['answer'], data['mctype'])
        elif qtype == 'TypeIn':
            q = TypeIn(data['answer'])
        elif qtype == 'Ranking':
            q = Ranking(data['items'])
        elif qtype == 'Matching':
            q = Matching(data['items'])
        else:
            q = None

        if q and 'text' in data and 'subject' in data and 'weight' in data:
            q.text = data['text']
            q.sub = data['subject']        
            q.weight = data['weight']
        
        if q and 'hints' in data:
            for text in data['hints']:
                h = Hint(text)
                q.hints.append(h)

        return q


class TypeIn(Question):
    __tablename__ = 'type_in'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    answer = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity':'type_in'
    }

    def __init__(self, answer):
        self.answer = answer

    def __repr__(self):
        return 'Type In Question %s' % self.id

class MultipleChoice(Question):
    """ This is the multiple choice question class """
    __tablename__ = 'multiple_choice'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    mctype = db.Column(db.String(1))
    choices = db.relationship('MCAnswer', backref='multiple_choice')

    __mapper_args__ = {
        'polymorphic_identity':'multiple_choice'
    }

    def __init__(self, answers, mctype):
        self.mctype = mctype
        for answer in answers:
            a = MCAnswer(answer['text'], answer['correct'])
            self.choices.append(a)

    def __repr__(self):
        return 'Multiple Choice Question %s' % (self.id)

class MCAnswer(db.Model):
    """ This is the multiple choice answer class """
    __tablename__ = 'mcanswer'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    correct = db.Column(db.Boolean())
    mcid = db.Column(db.Integer, db.ForeignKey('multiple_choice.id'))

    def __init__(self, text, correct):
        self.text = text
        self.correct = correct

    def __repr__(self):
        return 'Multiple Choice Answer %s' % (self.id)

class Ranking(Question):
    __tablename__ = 'ranking'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    items = db.relationship('RankItem', backref='ranking')

    __mapper_args__ = {
        'polymorphic_identity':'ranking'
    }

    def __init__(self, items):
        for rank, text in enumerate(items):
            ri = RankItem(rank, text)
            self.items.append(ri)

    def __repr__(self):
        return 'Ranking Question %s' % (self.id)

class RankItem(db.Model):
    __tablename__ = 'rank_item'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    rank = db.Column(db.Integer)
    rid = db.Column(db.Integer, db.ForeignKey('ranking.id'))

    def __init__(self, rank, text):
        self.rank = rank
        self.text = text

    def __repr__(self):
        return 'Ranking Item %s' % (self.id)

class Matching(Question):
    __tablename__ = 'matching'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    items = db.relationship('MatchItem', backref='matching')

    __mapper_args__ = {
        'polymorphic_identity':'matching'
    }

    def __init__(self, items):
        for text, answer in items:
            mi = MatchItem(text, answer)
            self.items.append(mi)

    def __repr__(self):
        return 'Matching Question %s' % (self.id)

class MatchItem(db.Model):
    __tablename__ = 'match_item'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    answer = db.Column(db.String(255))
    mid = db.Column(db.Integer, db.ForeignKey('matching.id'))

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

    def __repr__(self):
        return 'Matching Item %s' % (self.id)

class Hint(db.Model):
    __tablename__ = 'hint'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    qid = db.Column(db.ForeignKey('question.id'))

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Hint %s' % (self.id)
