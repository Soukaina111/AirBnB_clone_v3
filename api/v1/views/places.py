#!/usr/bin/python3
"""Module pour gérer toutes les actions par
défaut de l'API RESTFul pour les objets Place"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def func_getplaces(city_id):
    """Récupère la liste de tous les objets Place d'une City"""
    # Récupère la City avec l'ID donné depuis le stockage
    city = storage.get(City, city_id)
    # Si la City n'est pas trouvée, retourne une erreur 404
    if city is None:
        abort(404)
    # Récupère tous les objets Place liés à la City depuis le stockage
    places = [place.to_dict() for place in city.places]
    # Retourne la liste des objets Place en JSON
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def func_getplace(place_id):
    """Récupère un objet Place"""
    # Récupère l'objet Place avec l'ID donné depuis le stockage
    place = storage.get(Place, place_id)
    # Si l'objet Place n'est pas trouvé, retourne une erreur 404
    if place is None:
        abort(404)
    # Sérialise l'objet Place en JSON et retourne la réponse
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def func_deleteplace(place_id):
    """Supprime un objet Place"""
    # Récupère l'objet Place avec l'ID donné depuis le stockage
    place = storage.get(Place, place_id)
    # Si l'objet Place n'est pas trouvé, retourne une erreur 404
    if place is None:
        abort(404)
    # Supprime l'objet Place du stockage et enregistre les modifications
    storage.delete(place)
    storage.save()
    # Retourne une réponse vide avec le code d'état 200
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def func_createplace(city_id):
    """Crée un objet Place"""
    # Récupère les données JSON de la requête
    dtreqjson = request.get_json()
    # Si les données de la requête ne sont pas en JSON ou la
    # clé 'user_id' ou 'name' est manquante, retourne une erreur 400
    if dtreqjson is None:
        abort(400, "Not a JSON")
    if 'user_id' not in dtreqjson:
        abort(400, "Missing user_id")
    if 'name' not in dtreqjson:
        abort(400, "Missing name")
    # Récupère la City avec l'ID donné depuis le stockage
    city = storage.get(City, city_id)
    # Si la City n'est pas trouvée, retourne une erreur 404
    if city is None:
        abort(404)
    # Récupère l'objet User avec l'ID donné depuis le stockage
    user = storage.get(User, dtreqjson['user_id'])
    # Si l'objet User n'est pas trouvé, retourne une erreur 404
    if user is None:
        abort(404)
    # Crée un nouvel objet Place avec les données de la requête
    new_place = Place(city_id=city_id, **dtreqjson)
    # Enregistre le nouvel objet Place dans le stockage
    new_place.save()
    # Sérialise le nouvel objet Place en JSON et retourne la réponse
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def func_updateplace(place_id):
    """Met à jour un objet Place"""
    # Récupère l'objet Place avec l'ID donné depuis le stockage
    place = storage.get(Place, place_id)
    # Si l'objet Place n'est pas trouvé, retourne une erreur 404
    if place is None:
        abort(404)
    # Récupère les données JSON de la requête
    dtreqjson = request.get_json()
    # Si les données de la requête ne sont pas en JSON, retourne une erreur 400
    if dtreqjson is None:
        abort(400, "Not a JSON")
    # Liste des clés à ignorer lors de la mise à jour
    ignrkeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    # Met à jour l'objet Place avec les données de la requête
    for ky, vlue in dtreqjson.items():
        if ky not in ignrkeys:
            setattr(place, ky, vlue)
    # Enregistre l'objet Place mis à jour dans le stockage
    place.save()
    # Sérialise l'objet Place mis à jour en JSON et retourne la réponse
    return jsonify(place.to_dict()), 200
