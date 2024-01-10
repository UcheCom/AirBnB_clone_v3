#!/usr/bin/python3
"""Handles  API actions on Place objects"""

from models.state import State
from models.amenity import Amenity
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
    """updates a place"""
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
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """ This retrieves all Place objects depending of the JSON
    in the body of the request
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    body = request.get_json()

    if body and len(body):
        states = body.get('states', None)
        cities = body.get('cities', None)
        amenities = body.get('amenities', None)

    if not body or not len(body) or (
            not states and
            not cities and
            not amenities):
        places = storage.all('Place').values()
        place_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)

    places_list = []

    if states:
        states_obj = [storage.get(State, state_id) for state_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places_list.append(place)

    if cities:
        city_obj = [storage.get(City, city_id) for city_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, an_id) for an_id in amenities]

        places_list = [place for place in places_list
                       if all([amen in place.amenities
                               for amen in amenities_obj])]

    places = []
    for plac in places_list:
        p = plac.to_dict()
        p.pop('amenities', None)
        places.append(p)

    return jsonify(places)
