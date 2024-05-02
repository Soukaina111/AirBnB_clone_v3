#!/usr/bin/python3
''' Let's create an Amenity view'''

from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from os import name
from models.amenity import Amenity
# add
from models import storage

# app = Flask(__name__)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def func_getamenities():
    """Retrieves the list
    of all Amenity objects."""
    # Récupère tous les objets Amenity de la base de données
    amenities = storage.all(Amenity).values()
    # Convertit les objets Amenity en dictionnaires JSON et les retourne
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def func_getamenity(amenity_id):
    """Retrieves an Amenity
    object by its ID."""
    # Récupère l'objet Amenity correspondant à amenity_id
    dataamenity = storage.get('Amenity', amenity_id)
    # Si l'objet Amenity n'existe pas, retourne une erreur 404
    if dataamenity is None:
        abort(404)
    else:
        # Convertit l'objet Amenity en dictionnaire JSON et le retourne
        return jsonify(dataamenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def func_deleteamenity(amenity_id):
    """Deletes an Amenity
    object by its ID."""
    # Récupère l'objet Amenity correspondant à amenity_id
    dataamenity = storage.get('Amenity', amenity_id)
    # Si l'objet Amenity n'existe pas
    # retourne une erreur 404
    if dataamenity is None:
        abort(404)
    # Supprime l'objet Amenity de la base de données
    # enregistre les changements
    storage.delete(dataamenity)
    storage.save()
    # Retourne une réponse vide
    # avec le code d'état 200
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def func_createamenity():
    """Creates a new Amenity object."""
    # Récupère les données JSON de la requête HTTP
    datareq_json = request.get_json()
    # Si les données JSON sont invalides, retourne une erreur 400
    if datareq_json is None:
        abort(400, "Not a JSON")
    # Si la clé 'name' est absente des données JSON
    # retourne une erreur 400
    if 'name' not in datareq_json:
        abort(400, "Missing name")
    # Crée un nouvel objet Amenity avec
    # les données JSON et l'enregistre
    nw_amenity = Amenity(**datareq_json)
    nw_amenity.save()
    # Retourne le nouvel objet Amenity converti
    # en dictionnaire JSON avec le code d'état 201
    return jsonify(nw_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def func_updateamenity(amenity_id):
    """Updates an Amenity object by its ID."""
    # Récupère l'objet Amenity correspondant à amenity_id
    amenity = storage.get('Amenity', amenity_id)
    # Si l'objet Amenity n'existe pas, retourne une erreur 404
    if amenity is None:
        abort(404)
    # Récupère les données JSON de la requête HTTP
    datareq_json = request.get_json()
    # Si les données JSON sont invalides, retourne une erreur 400
    if datareq_json is None:
        abort(400, "Not a JSON")
    # Liste des clés à ignorer lors de la mise à jour de l'objet Amenity
    ignrkeys = ['id', 'created_at', 'updated_at']
    # Parcourt les clés et valeurs des données JSON
    for key, value in datareq_json.items():
        # Si la clé n'est pas dans la liste des clés à ignorer,
        # met à jour l'attribut correspondant de l'objet Amenity
        if key not in ignrkeys:
            setattr(amenity, key, value)
    # Enregistre les changements effectués sur l'objet Amenity
    amenity.save()
    # Retourne l'objet Amenity mis à jour converti
    # en dictionnaire JSON avec le code d'état 200
    return jsonify(amenity.to_dict()), 200
