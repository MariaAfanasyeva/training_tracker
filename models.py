from app import db


class Distance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Numeric(10, 2))
    units = db.Column(db.String(100))
    sets = db.relationship('Set', backref='distance', lazy=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    exercises = db.relationship('Exercise', backref='group', lazy=True)


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training_date = db.Column(db.Date)
    status = db.Column(db.String(255))
    sets = db.relationship('Set', backref='training', lazy=True)


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(10, 2))
    units = db.Column(db.String(100))
    sets = db.relationship('Set', backref='weight', lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    sets = db.relationship('Set', backref='exercise', lazy=True)


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_count = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'), nullable=False)
    distance_id = db.Column(db.Integer, db.ForeignKey('distance.id'), nullable=True)
    weight_id = db.Column(db.Integer, db.ForeignKey('weight.id'), nullable=True)