#!/usr/bin/python3

"""
Module Status of API
End point that returns the status of API

"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})  # allow CORS

app.register_blueprint(app_views)

# make json pretty
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

HBNB_API_HOST = os.environ.get('HBNB_API_HOST')
HBNB_API_PORT = os.environ.get('HBNB_API_POR')


@app.teardown_appcontext
def teardown_db(response_or_exc):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(error='Not found'), 404)

if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
