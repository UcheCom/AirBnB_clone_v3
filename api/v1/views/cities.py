#!/usr/bin/python3
""" Creation of new view for City object """

from models.city import City
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def city_get_all(state_id):
    """ This retrieves all city objects from a state
    returns json for all states
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict() for city in state.cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_get(city_id):
    """Retrieves a ctiy"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_del(city_id):
    """ This deletes a city object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def city_create(state_id):
    """ This creates a city in a state """
    state = storage.get('State', state_id)
    if not state:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")
    if "name" not in json:
        abort(400, "Missing name")

    city = City(**json)
    setattr(city, 'state_id', state_id)
    storage.new(City)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(state_id):
    """This updates a State object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
