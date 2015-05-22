from app import db

class Threshold(db.Model):
    __tablename__ = 'threshold'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    goal = db.Column(db.Integer)
    next = db.Column(db.Integer, db.ForeignKey('threshold.id'))
    subjects = db.relationship('Subject', backref='threshold')

    def __init__(self, data):
        self.name = data['name']
        next = Threshold.query.filter_by(name=data.get('next', None)).first()
        if next:
            self.next = next.id
        self.goal = data.get('goal', 0)

    def __repr__(self):
        return self.name

    def is_open(self, user):
        t = Threshold.query.filter_by(next=self.id).first()
        if all([s in user.completed for s in t.subjects]):
            return True
        return False

    @staticmethod
    def from_dict(data):
        return Threshold(data)

    @staticmethod
    def make_list(user):
        thresholds = []
        subquery = db.session.query(Threshold.next).filter(Threshold.next != None)
        t = db.session.query(Threshold).filter(~Threshold.id.in_(subquery)).first()
        t.open = True
        thresholds.append(t)
        while t.next != None:
            tnext = Threshold.query.get(t.next)
            if all([s in user.completed for s in t.subjects]):
                tnext.open = True
            else:
                tnext.open = False
            thresholds.append(tnext)
            t = tnext
        return thresholds

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    text = db.Column(db.Text())
    goal = db.Column(db.Integer)
    thres = db.Column(db.Integer, db.ForeignKey('threshold.id'))
    questions = db.relationship('Question', backref='subject')

    def __init__(self, data):
        self.name = data['name']
        self.text = data['text']
        thres = Threshold.query.filter_by(name=data.get('threshold', None)).first()
        if thres:
            self.thres = thres.id
        self.goal = data.get('goal', 0)

    def __repr__(self):
        return self.name

    @staticmethod
    def make_queue(sid):
        sub = Subject.query.get(sid)
        qs = sub.questions
        return [q.id for q in qs]

    @staticmethod
    def from_dict(data):
        return Subject(data)

class Question(db.Model):
    """ This is the Question base class """
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    text = db.Column(db.Text())
    weight = db.Column(db.Integer, default=0)
    sub = db.Column(db.Integer, db.ForeignKey('subject.id'))
    hints = db.relationship('Hint', backref='question', cascade='save-update, delete')

    __mapper_args__ = {
        'polymorphic_identity':'question',
        'polymorphic_on':type
    }

    def __init__(self, data):
        self.text = data['text']
        self.weight = data['weight']
        sub = Subject.query.filter_by(name=data.get('subject', None)).first()
        if sub:
            self.sub = sub.id
        for text in data['hints']:
            h = Hint(text)
            self.hints.append(h)

    def __repr__(self):
        return 'Question %s' % (self.id)

    @staticmethod
    def from_dict(data):
        type = data.get('type', None)
        if type == 'MultipleChoice':
            q = MultipleChoice(data)
        elif type == 'TypeIn':
            q = TypeIn(data)
        elif type == 'Ranking':
            q = Ranking(data)
        elif type == 'Matching':
            q = Matching(data)
        elif type == 'Coding':
            q = Coding(data)
        else:
            q = None
        return q


class TypeIn(Question):
    __tablename__ = 'type_in'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    answer = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity':'type_in'
    }

    def __init__(self, data):
        Question.__init__(self, data)
        self.answer = data['answer']

    def __repr__(self):
        return 'Type In Question %s' % self.id

class MultipleChoice(Question):
    """ This is the multiple choice question class """
    __tablename__ = 'multiple_choice'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    #mctype = db.Column(db.String(1))
    mctype = db.Column(db.Enum('1', 'X', name='mctype_check'))
    choices = db.relationship('MCAnswer', backref='multiple_choice', cascade='save-update, delete')

    __mapper_args__ = {
        'polymorphic_identity':'multiple_choice'
    }

    def __init__(self, data):
        Question.__init__(self, data)
        self.mctype = data['mctype']
        for answer in data['choices']:
            a = MCAnswer(answer)
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

    def __init__(self, answer):
        self.text = answer['text']
        self.correct = answer['correct']

    def __repr__(self):
        return 'Multiple Choice Answer %s' % (self.id)

class Ranking(Question):
    __tablename__ = 'ranking'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    items = db.relationship('RankItem', backref='ranking', cascade='save-update, delete')

    __mapper_args__ = {
        'polymorphic_identity':'ranking'
    }

    def __init__(self, data):
        Question.__init__(self, data)
        for rank, text in enumerate(data['items']):
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
    items = db.relationship('MatchItem', backref='matching', cascade='save-update, delete')

    __mapper_args__ = {
        'polymorphic_identity':'matching'
    }

    def __init__(self, data):
        Question.__init__(self, data)
        for i in range(len(data['texts'])):
            mi = MatchItem(data['texts'][i], data['answers'][i])
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

class Coding(Question):
    __tablename__ = 'coding'
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    code = db.Column(db.Text())
    exec_name = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity':'coding'
    }

    def __init__(self, data):
        Question.__init__(self, data)
        self.code = data['code']
        self.exec_name = data['exec_name']

    def __repr__(self):
        return 'Coding Question %s' % self.id
