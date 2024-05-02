#!/usr/bin/python3
"""Module pour gérer toutes les actions par défaut de
l'API RESTFul pour les objets Review liés aux Places"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def func_getreviews(place_id):
    """Récupère la liste de tous les objets Review liés à une Place"""
    # Récupère la Place avec l'ID donné depuis le stockage
    place = storage.get(Place, place_id)
    # Si la Place n'est pas trouvée, retourne une erreur 404
    if place is None:
        abort(404)
    # Récupère tous les objets Review liés à la Place depuis le stockage
    reviews = [review.to_dict() for review in place.reviews]
    # Retourne la liste des objets Review en JSON
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def func_getreview(review_id):
    """Récupère un objet Review"""
    # Récupère l'objet Review avec l'ID donné depuis le stockage
    review = storage.get(Review, review_id)
    # Si l'objet Review n'est pas trouvé, retourne une erreur 404
    if review is None:
        abort(404)
    # Sérialise l'objet Review en JSON et retourne la réponse
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def func_deletereview(review_id):
    """Supprime un objet Review"""
    # Récupère l'objet Review avec l'ID donné depuis le stockage
    review = storage.get(Review, review_id)
    # Si l'objet Review n'est pas trouvé, retourne une erreur 404
    if review is None:
        abort(404)
    # Supprime l'objet Review du stockage et enregistre les modifications
    storage.delete(review)
    storage.save()
    # Retourne une réponse vide avec le code d'état 200
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def func_createreview(place_id):
    """Crée un objet Review"""
    # Récupère les données JSON de la requête
    dtrqjson = request.get_json()
    # Si les données de la requête ne sont pas en JSON ou la clé
    # 'user_id' ou 'text' est manquante, retourne une erreur 400
    if dtrqjson is None:
        abort(400, "Not a JSON")
    if 'user_id' not in dtrqjson:
        abort(400, "Missing user_id")
    if 'text' not in dtrqjson:
        abort(400, "Missing text")
    # Récupère la Place avec l'ID donné depuis le stockage
    place = storage.get(Place, place_id)
    # Si la Place n'est pas trouvée, retourne une erreur 404
    if place is None:
        abort(404)
    # Récupère l'objet User avec l'ID donné depuis le stockage
    user = storage.get(User, dtrqjson['user_id'])
    # Si l'objet User n'est pas trouvé, retourne une erreur 404
    if user is None:
        abort(404)
    # Crée un nouvel objet Review avec les données de la requête
    new_review = Review(place_id=place_id, **dtrqjson)
    # Enregistre le nouvel objet Review dans le stockage
    new_review.save()
    # Sérialise le nouvel objet Review en JSON et retourne la réponse
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def func_updatereview(review_id):
    """Met à jour un objet Review"""
    # Récupère l'objet Review avec l'ID donné depuis le stockage
    review = storage.get(Review, review_id)
    # Si l'objet Review n'est pas trouvé, retourne une erreur 404
    if review is None:
        abort(404)
    # Récupère les données JSON de la requête
    dtrqjson = request.get_json()
    # Si les données de la requête ne sont pas en JSON,
    # retourne une erreur 400
    if dtrqjson is None:
        abort(400, "Not a JSON")
    # Liste des clés à ignorer lors de la mise à jour
    ignrkeys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    # Met à jour l'objet Review avec les données de la requête
    for ky, vlue in dtrqjson.items():
        if ky not in ignrkeys:
            setattr(review, ky, vlue)
    # Enregistre l'objet Review mis à jour dans le stockage
    review.save()
    # Sérialise l'objet Review mis à jour en JSON et retourne la réponse
    return jsonify(review.to_dict()), 200
