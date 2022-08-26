import datetime

from app import db


class Distance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Numeric(10, 2))
    units = db.Column(db.String(100))
    sets = db.relationship("Set", backref="distance", lazy=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    exercises = db.relationship("Exercise", backref="group", lazy=True)


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training_date = db.Column(db.Date, default=datetime.datetime.now)
    status = db.Column(db.String(255))
    sets = db.relationship("Set", backref="training", lazy=True)
    users = db.relationship("User", backref="training", lazy=True)


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(10, 2))
    units = db.Column(db.String(100))
    sets = db.relationship("Set", backref="weight", lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id", ondelete="SET NULL"), nullable=True)
    sets = db.relationship("Set", backref="exercise", lazy=True)


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_count = db.Column(db.Integer, nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey("training.id", ondelete="CASCADE"), nullable=False)
    distance_id = db.Column(db.Integer, db.ForeignKey("distance.id", ondelete="CASCADE"), nullable=True)
    weight_id = db.Column(db.Integer, db.ForeignKey("weight.id", ondelete="CASCADE"), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    training_id = db.Column(db.Integer, db.ForeignKey("training.id"))
    is_active = db.Column(db.Boolean)
    password = db.Column(db.String(255))
    created_at = db.Column(db.Date, default=datetime.datetime.now)
