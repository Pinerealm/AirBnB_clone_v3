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


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a amenity object, linked to a place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        return jsonify({"error": "Not found"}), 404

    if storage_t == 'db':
        if amenity not in place.amenities:
            return jsonify({"error": "Not found"}), 404
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    else:
        if amenity_id not in place.amenity_ids:
            return jsonify({"error": "Not found"}), 404
        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Links a amenity object to a place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        return jsonify({"error": "Not found"}), 404

    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        storage.save()
        return jsonify(amenity.to_dict()), 201
