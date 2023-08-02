#!/usr/bin/python3
"""The Amenity view module
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """Returns a JSON string containing all amenity objects
    """
    amenities = storage.all("Amenity")
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity(amenity_id):
    """Returns a JSON string containing an amenity object
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an amenity object
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates an amenity object
    """
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an amenity object
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
