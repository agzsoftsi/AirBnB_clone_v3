#!/usr/bin/python3
"""
Module View Cities
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """ GET method to retrieve list of all City objects of State"""
    all_cities = []
    if not storage.get('State', state_id):
        abort(404)
    for city in storage.all('City').values():
        if state_id == city.to_dict()['state_id']:
            all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def retrieve_city(city_id):
    """ Method GET to retrieve a particular City """
    city = storage.get('City', city_id)
    if city:
        return city.to_dict()
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ DELETE Method to delete a City """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return {}
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ POST MEthod to create a City """
    city_name = request.get_json()
    if not storage.get('State', state_id):
        abort(404)
    if not city_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in city_name:
        abort(400, {'Missing name'})
    city_name['state_id'] = state_id
    new_city = City(**city_name)
    storage.new(new_city)
    storage.save()
    return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ PUT Method to update a City """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_city = storage.get('City', city_id)
    if not my_city:
        abort(404)
    for key, value in update_attr.items():
        setattr(my_city, key, value)
    storage.save()
    return my_city.to_dict()
