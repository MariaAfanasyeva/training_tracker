from flask import Blueprint, jsonify, make_response, request

from app import db
from models import Training
from schemas import training_schema, trainings_schema
from services.auth import login_required, user_is_admin, user_is_author

training = Blueprint("training", __name__)


@training.route("/trainings", methods=["GET"])
def get_all_trainings():
    trainings = Training.query.all()
    result = trainings_schema.dump(trainings)
    return make_response(result)


@training.route("/training/<training_id>", methods=["GET"])
def get_training_by_id(training_id):
    training = Training.query.get(training_id)
    if training is not None:
        result = training_schema.dump(training)
        return make_response(result)
    else:
        return make_response(jsonify({"message": "Invalid training id"}), 500)


@training.route("/training", methods=["POST"])
@login_required
def create_training(current_user):
    status = "started"
    user_id = current_user.id
    new_training = Training(status=status, user_id=user_id)
    db.session.add(new_training)
    db.session.commit()
    return make_response(training_schema.dump(new_training), 201)


@training.route("/training/<training_id>", methods=["DELETE"])
@login_required
def delete_training(current_user, training_id):
    training = Training.query.get(training_id)
    if training is not None:
        if user_is_admin(current_user) or training.user_id == current_user.id:
            db.session.delete(training)
            db.session.commit()
            return make_response(jsonify({"message": "Training deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can delete the training"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid training id"}), 500)


@training.route("/training/<training_id>", methods=["PUT"])
@login_required
def update_training(current_user, training_id):
    training = Training.query.get(training_id)
    if training is not None:
        if user_is_admin(current_user) or training.user_id == current_user.id:
            status = request.json["status"]
            training.status = status
            db.session.commit()
            return make_response(training_schema.dump(training), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can edit training"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid training id"}), 500)
