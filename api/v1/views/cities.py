#!/usr/bin/python3
"""The City view module
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities(state_id):
    """Returns a JSON string containing all the cities in a state
    """
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Handles GET, DELETE and PUT requests for a city object
    """
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(city.to_dict())
    
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    
    if request.method == 'PUT':
        data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """Creates a city object, linked to a state
    """
    state = storage.get("State", state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201
