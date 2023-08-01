#!/usr/bin/python3
"""The index module
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON string with the status
    """
    return jsonify({"status": "OK"})
