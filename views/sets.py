from flask import Blueprint, jsonify, make_response, request

from app import db
from models import Set
from schemas import set_schema, sets_schema
from services.auth import login_required, user_is_admin, user_is_author

set = Blueprint("set", __name__)


@set.route("/sets", methods=["GET"])
def get_all_sets():
    sets = Set.query.all()
    result = sets_schema.dump(sets)
    return make_response(result)


@set.route("/set/<set_id>", methods=["GET"])
def get_set_by_id(set_id):
    set = Set.query.get(set_id)
    if set is not None:
        result = set_schema.dump(set)
        return make_response(result)
    else:
        return make_response(jsonify({"message": "Invalid set id"}), 500)


@set.route("/set", methods=["POST"])
@login_required
def create_set(current_user):
    exercise_count = request.json["exercise_count"]
    exercise_id = request.json["exercise_id"]
    training_id = request.json["training_id"]
    distance_id = request.json.get("distance_id")
    weight_id = request.json.get("weight_id")
    new_set = Set(
        exercise_count=exercise_count,
        training_id=training_id,
        exercise_id=exercise_id,
        distance_id=distance_id,
        weight_id=weight_id,
        added_by=current_user.id,
    )
    db.session.add(new_set)
    db.session.commit()
    return make_response(set_schema.dump(new_set), 201)


@set.route("/set/<set_id>", methods=["DELETE"])
@login_required
def delete_set(current_user, set_id):
    set = Set.query.get(set_id)
    if set is not None:
        if user_is_admin(current_user) or user_is_author(current_user, set):
            db.session.delete(set)
            db.session.commit()
            return make_response(jsonify({"message": "Set deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can delete the set"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid set id"}), 500)


@set.route("/set/<set_id>", methods=["PUT"])
@login_required
def update_set(current_user, set_id):
    set = Set.query.get(set_id)
    if set is not None:
        if user_is_admin(current_user) or user_is_author(current_user, set):
            exercise_count = request.json["exercise_count"]
            exercise_id = request.json["exercise_id"]
            training_id = request.json["training_id"]
            distance_id = request.json.get("distance_id")
            weight_id = request.json.get("weight_id")
            set.exercise_count = exercise_count
            set.exercise_id = exercise_id
            set.training_id = training_id
            set.distance_id = distance_id
            set.weight_id = weight_id
            db.session.commit()
            return make_response(set_schema.dump(set), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can edit set"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid set id"}), 500)
