#!/usr/bin/python3
""" Module for index """

from api.v1.views import app_views
from flask import jsonify


def status():
    """ defining the status of the api """
    return jsonify({"status": "OK"})
