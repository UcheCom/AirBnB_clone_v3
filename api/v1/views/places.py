#!/usr/bin/python3
"""Handles  API actions on Place objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve all places in a specified city"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """retrieves a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ This deletes a place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """Creates a new place"""
    city = storage.get("City", city_id)
    if not None:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")
    if "user_id" not in json:
        abort(400, "Missing user_id")
    user = storage.get("User", json['user_id'])
    if not user:
        abort(404)
    if "name" not in json:
        abort(400, 'Missing name')
    json['city_id'] = city_id
    place = Place(**json)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_update(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
