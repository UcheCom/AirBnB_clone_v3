#!/usr/bin/python3
"""Handles API actions on Place Review objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """This retrieves list of all review objs for a place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """retrieve a review based on his ID"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_del(place_id):
    """ This deletes a place object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def place_create(place_id):
    """Creates a new place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")
    if "user_id" not in json:
        abort(400, "Missing user_id")
    user = storage.get("User", json['user_id'])
    if not user:
        abort(404)
    if "text" not in json:
        abort(400, 'Missing text')
    json['place_id'] = place_id
    review = Review(**json)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update(review_id):
    """This updates a review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    json = request.get_json()
    if not json:
        abort(400, "Not a JSON")

    for key, value in json.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
