#!/usr/bin/python3

"""
Module View States

"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('states', strict_slashes=False)
def all_states():
    """ GET Method to retrieve list of all State objects """
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def retrieve_state(state_id):
    """ GET Method to retrieve a particular State using id"""
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
        return state
    except:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ DELETE Method to delete a State """
    state = storage.get('State', state_id)
    if state:
        state.delete()
        storage.save()
        return {}
    abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ POST Method to create a State """
    state_name = request.get_json()
    if not state_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in state_name:
        abort(400, {'Missing name'})
    new_state = State(**state_name)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ PUT Method to update a State """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_state = storage.get('State', state_id)
    if not my_state:
        abort(404)
    for key, value in update_attr.items():
        setattr(my_state, key, value)
    storage.save()
    return my_state.to_dict()
