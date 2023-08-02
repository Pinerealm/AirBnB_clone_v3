#!/usr/bin/python3
"""The Place view module
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places(city_id):
    """Returns a JSON string containing all the places in a city
    """
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place(place_id):
    """Handles GET, DELETE and PUT requests for a place object
    """
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """Creates a place object, linked to a city
    """
    city = storage.get("City", city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("user_id") is None:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get("User", data.get("user_id"))
    if user is None:
        return jsonify({"error": "Not found"}), 404

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201
