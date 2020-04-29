#!/usr/bin/python3
"""
Module View Places
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places_by_city(city_id):
    """ GET Method retrieve list of all Places in City  objects """
    city = storage.get('City', city_id)
    if city:
        places = city.places
        all_places = []

        for place in places:
            all_places.append(place.to_dict())
        return jsonify(all_places)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def retrieve_place(place_id):
    """ GET Method to retrieve a particular Places """
    place = storage.get('Place', place_id)
    if place:
        return place.to_dict()
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ DELETE Method delete a Place """
    place = storage.get('Place', place_id)

    if place:
        storage.delete(place)
        storage.save()
        return {}
    abort(404)
