#!/usr/bin/python3

"""
Module Status Index

"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """ Return status OK in json format for the Route"""

    return jsonify({'status': 'OK'})
