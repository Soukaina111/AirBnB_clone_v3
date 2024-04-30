#!/usr/bin/python3
''' Let's create a State view'''

from flask import abort, request, jsonify
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    """
    Retrieves all State objects and returns them as a JSON response.
    """
    states = storage.all('State')
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<string:state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieves a State object by its ID and returns it as a JSON response.
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object from the JSON request body.
    """
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    if "name" not in data:
        abort(400, {'error': 'Missing name'})
    state = State(name=data['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by its ID with the data from the JSON request body.
    """
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by its ID.
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
