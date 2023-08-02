#!/usr/bin/python3
"""The State view module
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """Returns a JSON string containing all state objects
    """
    states = storage.all("State")
    states = [state.to_dict() for state in states.values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    """Handles GET and DELETE and PUT requests for a state object
    """
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a state object
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201
