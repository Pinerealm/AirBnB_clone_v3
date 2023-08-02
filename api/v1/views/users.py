#!/usr/bin/python3
"""The User view module
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """Returns a JSON string containing all user objects
    """
    users = storage.all("User")
    users = [user.to_dict() for user in users.values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    """Handles GET and DELETE and PUT requests for a user object
    """
    user = storage.get("User", user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a user object
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("email") is None:
        return jsonify({"error": "Missing email"}), 400
    if data.get("password") is None:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201
