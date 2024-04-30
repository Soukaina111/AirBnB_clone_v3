#!/usr/bin/python3
''' Let's create a User view'''

from flask import Flask , abort , request
from api.v1.views import app_views
from os import name
from models.user import User

app = Flask(__name__)


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects.
    """
    users = User.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Retrieves a User object by its ID.
    """
    user = User.find(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object by its ID.
    """
    user = User.find(user_id)
    if not user:
        abort(404)
    user.delete()
    return jsonify({}), 200


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """
    Creates a new User object.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    if 'email' not in data or 'password' not in data:
        abort(400, {'error': 'Missing email or password'})
    user = User(email=data['email'], password=data['password'])
    user.save()
    return jsonify(user.to_dict()), 201


@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object by its ID.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    user = User.find(user_id)
    if not user:
        abort(404)
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save() # Save the updated user
    return jsonify(user.to_dict()), 200
