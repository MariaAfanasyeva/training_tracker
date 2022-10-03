from flask import Blueprint, jsonify, make_response, request

from app import db
from models import Group
from schemas import group_schema, groups_schema
from services.auth import login_required, user_is_admin, user_is_author

group = Blueprint("group", __name__)


@group.route("/groups", methods=["GET"])
def get_all_groups():
    groups = Group.query.all()
    result = groups_schema.dump(groups)
    return make_response(result)


@group.route("/group/<group_id>", methods=["GET"])
def get_group_by_id(group_id):
    group = Group.query.get(group_id)
    if group is not None:
        result = group_schema.dump(group)
        return make_response(result)
    else:
        return make_response(jsonify({"message": "Invalid group id."}), 500)


@group.route("/group", methods=["POST"])
@login_required
def create_group(current_user):
    group_name = request.json["group_name"]
    if Group.query.filter_by(name=group_name).first() is not None:
        return make_response(jsonify({"message": "Group with this name already exists"}), 401)
    new_group = Group(name=group_name, added_by=current_user.id)
    db.session.add(new_group)
    db.session.commit()
    return make_response(group_schema.dump(new_group), 201)


@group.route("/group/<group_id>", methods=["DELETE"])
@login_required
def delete_group(current_user, group_id):
    group = Group.query.get(group_id)
    if group is not None:
        if user_is_admin(current_user) or user_is_author(current_user, group):
            db.session.delete(group)
            db.session.commit()
            return make_response(jsonify({"message": "Group deleted"}), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can delete group"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid group id"}), 500)


@group.route("/group/<group_id>", methods=["PUT"])
@login_required
def update_group(current_user, group_id):
    group = Group.query.get(group_id)
    if group is not None:
        if user_is_admin(current_user) or user_is_author(current_user, group):
            new_group_name = request.json["new_group_name"]
            group.name = new_group_name
            db.session.commit()
            return make_response(group_schema.dump(group), 200)
        else:
            return make_response(jsonify({"message": "Only author or admin can edit group"}), 500)
    else:
        return make_response(jsonify({"message": "Invalid group id"}), 500)
