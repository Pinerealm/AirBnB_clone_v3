#!/usr/bin/python3
"""The Reviews view module
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews(place_id):
    """Returns a JSON string containing all the reviews associated with
    a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    """Handles GET, DELETE and PUT requests for a review object
    """
    review = storage.get("Review", review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """Creates a review object, linked to a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if data.get("user_id") is None:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get("User", data.get("user_id"))
    if user is None:
        return jsonify({"error": "Not found"}), 404

    if data.get("text") is None:
        return jsonify({"error": "Missing text"}), 400
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201
