#!/usr/bin/python3
""" Creation of new view for User object """

from models import storage
from models.user import User
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/userss", methods=['GET'], strict_slashes=False)
def users_get():
    """ This retrieves all User object """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_get(user_id):
    """ Retrieves a User object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_del(user_id):
    """ Deletes an Amenity object """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    user.delect()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a user"""
    json = request.get_json()
    if not json:
        abort(400, "Not a json")

    if 'email' not in json:
        abort(400, "Missing email")

    if 'password' not in json:
        abort(400, "Missing password")

    user = User(**json)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
