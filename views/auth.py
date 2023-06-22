from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models import User
from services.auth import create_tokens, use_refresh_token, verify_refresh_token
from schemas import user_schema, users_schema

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    password = request.json["password"]
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
        )
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
        return create_tokens(user.id)
    else:
        return make_response(jsonify({"message": "Invalid password"}), 401)


@auth.route("/refresh_token", methods=["POST"])
def refresh():
    access_token = request.json["access_token"]
    refresh_token = request.json["refresh_token"]
    if not access_token or not refresh_token:
        return make_response(jsonify({"message": "Tokens are missing"}), 401)
    if verify_refresh_token(access_token, refresh_token):
        return use_refresh_token(refresh_token)
    else:
        return make_response(jsonify({"message": "Invalid token"}), 401)


@auth.route("/users", methods=["GET"])
def get_all_users_data():
    users = User.query.all()
    result = users_schema.dump(users)
    return make_response(result)


@auth.route("/users/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user is not None:
        result  = user_schema.dump(user)
        return make_response(result)
    else: 
        return make_response(jsonify({"message": "Invalid user's id"}), 500)
    
