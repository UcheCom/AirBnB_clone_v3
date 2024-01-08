#!/usr/bin/python3
""" Module for index """

from api.v1.views import app_views
from flask import jsonify
from models import storage


# Task 3
@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ Defining the status of the api JSON response """
    return jsonify({'status': 'OK'})


# Task 4
@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    This retrieves the number of each objs based on type
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
