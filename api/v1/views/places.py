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


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ POST Method create a Place by City"""

    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    place_name = request.get_json()

    if not place_name:
        abort(400, {'Not a JSON'})
    if 'user_id' not in place_name:
        abort(400, {'Missing user_id'})
    if 'name' not in place_name:
        abort(400, {'Missing name'})

    user_id = request.get_json()["user_id"]
    user = storage.get('User', user_id)

    if user is None:
        abort(404)

    new_place = Place(**place_name)
    new_place.city_id = city.id
    new_place.user_id = user.id
    storage.new(new_place)
    storage.save()
    return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ PUT Method update a Place """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_place = storage.get('Place', place_id)
    if not my_place:
        abort(404)
    for key, value in update_attr.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(my_place, key, value)
    storage.save()
    return my_place.to_dict()
