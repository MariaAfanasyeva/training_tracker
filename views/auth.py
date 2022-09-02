import jwt
from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from models import User
from schemas import UserSchema

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    password = request.json["password"]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "Signup successful"}), 200)
    else:
        return make_response(jsonify({"message": "User with this email already exists"}), 202)


@auth.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    if not password or not email:
        return make_response(jsonify({"message": "Please enter your email address and password"}), 401)
    user = User.query.filter_by(email=email).first()
    if not user:
        return make_response(jsonify({"message": "User with this email doesn't exist"}), 401)
    if check_password_hash(user.password, password):
        # TODO: create function for creating refresh token (create file services.py) and implement login (return access and refresh token)
        pass
    else:
        return make_response(jsonify({"message": "Invalid password"}), 401)
