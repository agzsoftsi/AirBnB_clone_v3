#!/usr/bin/python3

"""
Module View States

"""

from models import storage
from flask import jsonify, make_response
from api.v1.views import app_views


@app_views.route("/states")
@app_views.route("/states/<state_id>")
def view_states(state_id=None):
    """ Return the list of states in json format by id

        Argument:
                state_id (str): id of object in State Class
        Return:
               json string with data of objects
    """

    states = storage.all("State").values()
    states_dict = []

    for state in states:
        if state_id is None:
            states_dict.append(state.to_dict())
        elif state.id == state_id:
            return jsonify(state.to_dict())

    if state_id is not None:
        return make_response(jsonify(error='Not found'), 404)

    return jsonify(states_dict)

@app_views.route("/states/<state_id>", methods=['DELETE'])
def view_delete(state_id=None):
    """ Delete state by id

        Argument:
                state_id (str): id of object in State Class
        Return:
               json string with status
    """

    states = storage.all("State").values()

    for state in states:
        if state.id == state_id:
            state.delete()
            return jsonify(state.to_dict()), 200


    return make_response(jsonify(error='Not found'), 404)
