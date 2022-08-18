from marshmallow import Schema, fields


class DistanceSchema(Schema):
    id = fields.Integer()
    distance = fields.Float()
    units = fields.String()


distance_schema = DistanceSchema()
distances_schema = DistanceSchema(many=True)


class GroupSchema(Schema):
    id = fields.Integer()
    name = fields.String()


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)


class TrainingSchema(Schema):
    id = fields.Integer()
    training_date = fields.Date()
    status = fields.String()


training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)


class WeightSchema(Schema):
    id = fields.Integer()
    weight = fields.Float()
    units = fields.String()


weight_schema = WeightSchema()
weights_schema = WeightSchema(many=True)


class ExerciseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    group_id = fields.Integer()


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)


class SetSchema(Schema):
    id = fields.Integer()
    exercise_count = fields.String()
    exercise_id = fields.Integer()
    training_id = fields.Integer()
    distance_id = fields.Integer()
    weight_id = fields.Integer()


set_schema = SetSchema()
sets_schema = SetSchema(many=True)


class UserSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    training_id = fields.Integer()
    is_active = fields.Boolean()
    created_at = fields.Date()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
