import datetime
from functools import wraps

import jwt
from flask import jsonify, make_response, request

from app import app
from models import User


def create_tokens(user_id):
    access_token_payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "grant_type": "access",
    }
    access_token = jwt.encode(access_token_payload, app.config["SECRET_KEY"], algorithm="HS256")
    access_token_encoded_payload = access_token.split(".")[0]
    refresh_token_key = access_token_encoded_payload[-8:]
    refresh_token_payload = {
        "key": refresh_token_key,
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1440),
        "grant_type": "refresh",
    }
    refresh_token = jwt.encode(refresh_token_payload, app.config["SECRET_KEY"], algorithm="HS256")
    return make_response(jsonify({"access_token": access_token, "refresh_token": refresh_token}))


def verify_refresh_token(access_token, refresh_token):
    try:
        refresh_token_data = jwt.decode(refresh_token, app.config["SECRET_KEY"], algorithms=["HS256"])
        if refresh_token_data["grant_type"] == "refresh":
            access_token_signature = access_token.split(".")[0][-8:]
            if refresh_token_data["key"] == access_token_signature:
                return True
        else:
            return False
    except Exception as e:
        return False


def use_refresh_token(refresh_token):
    data = jwt.decode(refresh_token, app.config["SECRET_KEY"], algorithms=["HS256"])
    new_tokens = create_tokens(data["user_id"])
    return new_tokens


def login_required(func):
    @wraps(func)
    def wrapped_login_required(*args, **kwargs):
        token = None
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization")
            if not token:
                return make_response(jsonify({"message": "Authentication Token is missing"}), 401)
            try:
                data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.get(data["user_id"])
                if current_user is None:
                    return make_response(jsonify({"message": "Invalid Authentication Token"}), 401)
            except Exception as e:
                return make_response(jsonify({"message": "Something went wrong"}), 500)
        return func(current_user, *args, **kwargs)

    return wrapped_login_required
