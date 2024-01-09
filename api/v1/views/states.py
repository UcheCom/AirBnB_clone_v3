#!/usr/bin/python3
""" Creation of new view for State object """

from models import storage
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_get_all(state_id=None):
    """ This retrieves all state objects or its id and
    returns json for all states
    """
    if not state_id:
        return jsonify([state.to_dict() for state in
                        storage.all(State).values()])

    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_del(state_id):
    """ This deletes a state object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def state_create():
    """ This creates a state object using API """
    state_dict = request.get_json()
    if not state_dict:
        abort(400, "Not a JSON")
    if "name" not in state_dict:
        abort(400, "Missing name")
    state = State(**state_dict)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """This updates a State object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
