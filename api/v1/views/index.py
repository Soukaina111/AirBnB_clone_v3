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
    listskv = {"amenities": "Amenity",
               "cities": "City",
               "places": "Place",
               "reviews": "Review",
               "states": "State",
               "users": "User"}
    alllist = {}
    for ky, vl in listskv.items():
        alllist[ky] = storage.count(vl)

    return jsonify(alllist)
