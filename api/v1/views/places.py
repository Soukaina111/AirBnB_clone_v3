#!/usr/bin/python3
from flask import abort, request, jsonify
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object by its ID
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object by its ID
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object associated with a City
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    if 'user_id' not in data:
        abort(400, {'error': 'Missing user_id'})

    user_id = data['user_id']
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, {'error': 'Missing name'})

    place = Place(name=data['name'], user_id=user_id, city_id=city_id)
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object by its ID
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
