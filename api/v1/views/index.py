#!/usr/bin/python3
"""The index module
"""
from flask import jsonify

from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON string with the status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns a JSON string containing the no of objects in each class
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
