from flask import Blueprint, jsonify, make_response, request

from extensions import db
from models import Weight
from schemas import weight_schema, weights_schema
from services.auth import login_required, user_is_admin, user_is_author

weight = Blueprint("weight", __name__)


@weight.route("/weights", methods=["GET"])
def get_all_weights():
    weight = Weight.query.all()
    result = weights_schema.dump(weight)
    return make_response(result)


@weight.route("/weight/<weight_id>", methods=["GET"])
def get_weight_by_id(weight_id):
    weight = Weight.query.get(weight_id)
    if weight is not None:
        result = weight_schema.dump(weight)
        return make_response(result)
    else:
        return make_response(jsonify({"message": "Invalid weight id"}), 500)


@weight.route("/weight", methods=["POST"])
@login_required
def create_weight(current_user):
    weight = request.json["weight"]
    units = request.json["units"]
    if Weight.query.filter_by(weight=weight, units=units).first() is not None:
        return make_response(jsonify({"message": "This weight already exists"}), 500)
    new_weight = Weight(weight=weight, units=units, added_by=current_user.id)
    db.session.add(new_weight)
    db.session.commit()
    return make_response(weight_schema.dump(new_weight), 201)


@weight.route("/weight/<weight_id>", methods=["DELETE"])
@login_required
def delete_weight(current_user, weight_id):
    weight = Weight.query.get(weight_id)
    if weight is not None:
        if user_is_admin(current_user) or user_is_author(current_user, weight):
            db.session.delete(weight)
            db.session.commit()
            return make_response(jsonify({"message": "Weight deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can delete the weight"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid weight id"}), 500)


@weight.route("/weight/<weight_id>", methods=["PUT"])
@login_required
def update_weight(current_user, weight_id):
    weight = Weight.query.get(weight_id)
    if weight is not None:
        if user_is_admin(current_user) or user_is_author(current_user, weight):
            new_weight_value = request.json["new_weight_value"]
            new_weight_unit = request.json["new_weight_unit"]
            weight.weight = new_weight_value
            weight.unit = new_weight_unit
            db.session.commit()
            return make_response(weight_schema.dump(weight), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can edit weight"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid weight id"}), 500)
