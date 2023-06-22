from flask import Blueprint, jsonify, make_response, request

from extensions import db
from models import Distance
from schemas import distance_schema, distances_schema
from services.auth import login_required, user_is_admin, user_is_author

distance = Blueprint("distance", __name__)


@distance.route("/distances", methods=["GET"])
def get_all_distances():
    distances = Distance.query.all()
    result = distances_schema.dump(distances)
    return make_response(result)


@distance.route("/distance/<distance_id>", methods=["GET"])
def get_distance_by_id(distance_id):
    distance = Distance.query.get(distance_id)
    if distance is not None:
        result = distance_schema.dump(distance)
        return make_response(result)
    else:
        return make_response(jsonify({"message": "Invalid distance id"}), 500)


@distance.route("/distance", methods=["POST"])
@login_required
def create_distance(current_user):
    distance = request.json["distance"]
    units = request.json["units"]
    if Distance.query.filter_by(distance=distance, units=units).first() is not None:
        return make_response(jsonify({"message": "This distance already exists"}), 500)
    new_distance = Distance(distance=distance, units=units, added_by=current_user.id)
    db.session.add(new_distance)
    db.session.commit()
    return make_response(distance_schema.dump(new_distance), 201)


@distance.route("/distance/<distance_id>", methods=["DELETE"])
@login_required
def delete_distance(current_user, distance_id):
    distance = Distance.query.get(distance_id)
    if distance is not None:
        if user_is_admin(current_user) or user_is_author(current_user, distance):
            db.session.delete(distance)
            db.session.commit()
            return make_response(jsonify({"message": "Distance deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can delete the distance"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid distance id"}), 500)


@distance.route("/distance/<distance_id>", methods=["PUT"])
@login_required
def update_distance(current_user, distance_id):
    distance = Distance.query.get(distance_id)
    if distance is not None:
        if user_is_admin(current_user) or user_is_author(current_user, distance):
            new_distance_value = request.json["new_distance_value"]
            new_distance_unit = request.json["new_distance_unit"]
            distance.distance = new_distance_value
            distance.units = new_distance_unit
            db.session.commit()
            return make_response(distance_schema.dump(distance), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can edit distance"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid distance id"}), 500)
