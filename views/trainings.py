from flask import Blueprint, jsonify, make_response, request

from app import db
from models import Training, User
from schemas import training_schema, trainings_schema
from services.auth import get_user_from_request, login_required

training = Blueprint("training", __name__)


@training.route("/trainings", methods=["GET"])
def get_all_trainings():
    trainings = Training.query.all()
    result = trainings_schema.dump(trainings)
    return make_response(result)
