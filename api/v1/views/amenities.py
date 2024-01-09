#!/usr/bin/python3
""" Creation of new view for Amenity object """

from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities_get():
    """ This retrieves all amenities """
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id):
    """ Retrieves a Amenity objec """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """ Deletes an Amenity object """
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    amenity.delect()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def amenity_create():
    """ This creates a amenity object using API """
    amenity_dict = request.get_json()
    if not amenity_dict:
        abort(400, "Not a JSON")
    if "name" not in amenity_dict:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_dict)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """This updates a Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
