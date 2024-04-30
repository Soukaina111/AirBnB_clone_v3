#!/usr/bin/python3
''' Let's create a User view'''

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_users():
    """
    Retrieves all User objects and returns them as a JSON response.
    """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<string:user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieves a User object by its ID and returns it as a JSON response.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object from the JSON request body.
    """
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    if email not in data:
        abort(400, {'error': 'Missing email'})
    if password not in data:
        abort(400, {'error': 'Missing password'})

    user = User(email=data['email'], password=data['password'])
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object by its ID with the data from the JSON request body.
    """
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by its ID.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
