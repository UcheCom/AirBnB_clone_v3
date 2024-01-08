#!/usr/bin/python3
""" Module: app """

from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """ Removes the current session obj after each request """
    storage.close()


# Task 5
@app.errorhandler(404)
def not_found(error):
    """ This returns JSON response with 'Not found' error message"""
    resp = {'error': 'Not found'}
    return jsonify(resp), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
