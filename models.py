import datetime

from app import db


class Distance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Numeric(10, 2))
    units = db.Column(db.String(100))
    added_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True, default=None)
    sets = db.relationship("Set", backref="distance", lazy=True)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    added_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True, default=None)
    exercises = db.relationship("Exercise", backref="group", lazy=True)


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training_date = db.Column(db.Date, default=datetime.datetime.now)
    status = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True, default=None)
    sets = db.relationship("Set", backref="training", lazy=True)


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(10, 2))
    units = db.Column(db.String(100))
    added_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True, default=None)
    sets = db.relationship("Set", backref="weight", lazy=True)


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id", ondelete="SET NULL"), nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True, default=None)
    sets = db.relationship("Set", backref="exercise", lazy=True)


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_count = db.Column(db.Integer, nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey("training.id", ondelete="CASCADE"), nullable=False)
    distance_id = db.Column(db.Integer, db.ForeignKey("distance.id", ondelete="CASCADE"), nullable=True)
    weight_id = db.Column(db.Integer, db.ForeignKey("weight.id", ondelete="CASCADE"), nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True, default=None)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    is_active = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=datetime.datetime.now)
    distancess = db.relationship("Distance", backref="user", lazy=True)
    groups = db.relationship("Group", backref="user", lazy=True)
    weights = db.relationship("Weight", backref="user", lazy=True)
    exercises = db.relationship("Exercise", backref="user", lazy=True)
