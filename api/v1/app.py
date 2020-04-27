#!/usr/bin/python3

"""
Module Status of API
End point that returns the status of API

"""

from models import storage
from api.v1.views import app_views
from flask import Flask
from flask import Blueprint
import os
app = Flask(__name__)

app.register_blueprint(app_views)

HBNB_API_HOST = os.environ.get('HBNB_API_HOST')
HBNB_API_PORT = os.environ.get('HBNB_API_POR')


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
