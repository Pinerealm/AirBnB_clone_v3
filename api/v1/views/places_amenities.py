#!/usr/bin/python3
"""The Places-Amenities view module.
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage, storage_t
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def place_amenities(place_id):
    """Returns a JSON string containing all the amenities associated with
    a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    if storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)
    else:
        amenities = [storage.get("Amenity", amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
        return jsonify(amenities)
