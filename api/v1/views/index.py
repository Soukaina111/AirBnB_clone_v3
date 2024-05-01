#!/usr/bin/python3
'''let's configure flask status'''
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    ''' shows the status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def get_statistics():
    """
    Endpoint to retrieve statistics about different entities in storage.
    Returns a JSON response with counts for each entity.
    """
    entity_counts = {
        'states': storage.count(State),
        'users': storage.count(User),
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review)
    }
    return jsonify(entity_counts)
