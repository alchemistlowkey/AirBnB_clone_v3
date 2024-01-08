#!/usr/bin/python3
"""
A view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves State objects with its ID
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    return jsonify(states.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes State object with its given ID
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    storage.delete(states)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    states = request.get_json()
    implement = State(**states)
    implement.save()
    return make_response(jsonify(implement.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State by its ID
    """
    states = storage.get(State, state_id)

    if not states:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    head_tag = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in head_tag:
            setattr(states, key, value)
    storage.save()
    return make_response(jsonify(states.to_dict()), 200)
