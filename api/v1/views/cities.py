#!/usr/bin/python3
''' Let's create a City view'''

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from os import name
from models.state import State
from models.city import City
from models import storage
import logging


"""app = Flask(__name__)"""


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def func_getcities(state_id):
    """Retrieves the list of all
    City objects for a specific State."""
    # Récupère l'objet State correspondant à state_id
    datastate = storage.get('State', state_id)
    # Si l'objet State n'existe pas, retourne une erreur 404
    if datastate is None:
        return abort(404)
    else:
        # Récupère la liste de tous les objets City liés à l'objet State
        datacities = [city.to_dict() for city in datastate.cities]
        return jsonify(datacities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def func_getcity(city_id):
    """Retrieves a City
    object by its ID."""
    # Récupère l'objet City correspondant à city_id
    datacity = storage.get('City', city_id)
    # Si l'objet City n'existe pas, retourne une erreur 404
    if datacity is None:
        return abort(404)
    return jsonify(datacity.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def func_deletecity(city_id):
    """Deletes a City object
    by its ID."""
    # Récupère l'objet City correspondant à city_id
    city = storage.get('City', city_id)
    # Si l'objet City n'existe pas, retourne une erreur 404
    if city is None:
        return abort(404)
    else:
        # Supprime l'objet City de la base de données
        # enregistre les changements
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def func_createcity(state_id):
    """Creates a new City object
    for a specific State."""
    """ loogiing"""
    logging.info(f"Request data: {request.get_json()}")
    logging.info(f"Content-Type: {request.content_type}")
    # Récupère l'objet State correspondant à state_id
    state = storage.get('State', state_id)
    # Si l'objet State n'existe pas, retourne une erreur 404
    if state is None:
        return abort(404)
    # Récupère les données JSON de la requête HTTP
    dtreq_json = request.get_json()
    # Si les données JSON sont invalides, retourne une erreur 400
    if dtreq_json is None:
        return abort(400, "Not a JSON")
    # Si la clé 'name' est absente des données JSON, retourne une erreur 400
    if 'name' not in dtreq_json:
        abort(400, "Missing name")
    # Ajoute state_id aux données JSON pour
    # créer une nouvelle City liée à l'objet State
    dtreq_json['state_id'] = state_id
    # Crée un nouvel objet City avec
    # les données JSON et l'enregistre
    nw_city = City(**dtreq_json)
    nw_city.save()
    return jsonify(nw_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def func_updatecity(city_id):
    """Updates a City object
    by its ID."""
    # Récupère l'objet City correspondant à city_id
    city = storage.get('City', city_id)
    # Si l'objet City n'existe pas, retourne une erreur 404
    if city is None:
        return abort(404)
    else:
        # Récupère les données JSON de la requête HTTP
        dtreq_json = request.get_json()
        # Si les données JSON sont invalides, retourne une erreur 400
        if dtreq_json is None:
            return abort(400, "Not a JSON")
            # Liste des clés à ignorer lors de la mise à jour de l'objet City
        ignrkeys = ['id', 'state_id', 'created_at', 'updated_at']
        # Parcourt les clés et valeurs des données JSON
        for key, value in dtreq_json.items():
            # Si la clé n'est pas dans la liste des clés à ignorer,
            # met à jour l'attribut correspondant de l'objet City
            if key not in ignrkeys:
                setattr(city, key, value)
        # Enregistre les changements effectués sur l'objet City
        city.save()
        return jsonify(city.to_dict()), 200
