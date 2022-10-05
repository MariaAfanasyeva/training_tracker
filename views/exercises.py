from flask import Blueprint, jsonify, make_response, request

from app import db
from models import Exercise
from schemas import exercise_schema, exercises_schema
from services.auth import login_required, user_is_admin, user_is_author

exercise = Blueprint("exercise", __name__)


@exercise.route("/exercises", methods=["GET"])
def get_all_exercises():
    exercises = Exercise.query.all()
    result = exercises_schema.dump(exercises)
    return make_response(result)


@exercise.route("/exercise/<exercise_id>", methods=["GET"])
def get_exercise_by_id(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is not None:
        result = exercise_schema.dump(exercise)
        return make_response(result)
    else:
        return make_response(jsonify({"message": "Invalid exercise id"}), 500)


@exercise.route("/exercise", methods=["POST"])
@login_required
def create_exercise(current_user):
    exercise_name = request.json["exercise_name"]
    exercise_group_id = request.json["exercise_group_id"]
    if Exercise.query.filter_by(name=exercise_name, group_id=exercise_group_id).first() is not None:
        return make_response(jsonify({"message": "This exercise already exists"}), 500)
    new_exercise = Exercise(name=exercise_name, group_id=exercise_group_id, added_by=current_user.id)
    db.session.add(new_exercise)
    db.session.commit()
    return make_response(exercise_schema.dump(new_exercise), 201)


@exercise.route("/exercise/<exercise_id>", methods=["DELETE"])
@login_required
def delete_exercise(current_user, exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is not None:
        if user_is_admin(current_user) or user_is_author(current_user, exercise):
            db.session.delete(exercise)
            db.session.commit()
            return make_response(jsonify({"message": "Exercise deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can delete the exercise"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid exercise id"}), 500)


@exercise.route("/exercise/<exercise_id>", methods=["PUT"])
@login_required
def update_exercise(current_user, exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise is not None:
        if user_is_admin(current_user) or user_is_author(current_user, exercise):
            new_exercise_name = request.json["new_exercise_name"]
            new_exercise_group_id = request.json["new_exercise_group_id"]
            exercise.name = new_exercise_name
            exercise.group_id = new_exercise_group_id
            db.session.commit()
            return make_response(exercise_schema.dump(exercise), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can edit exercise"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid exercise id"}), 500)
