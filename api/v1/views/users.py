#!/usr/bin/python3
''' Let's create a User view'''

from flask import abort, request, jsonify
from api.v1.views import app_views
from models.user import User
from models import storage

# app = Flask(__name__)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def func_getusers():
    """Récupère la liste de tous les objets User"""
    # Récupère tous les objets User depuis le stockage
    users = storage.all(User).values()
    # Sérialise les objets User en JSON et retourne la réponse
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def func_getuser(user_id):
    """ Récupère l'objet User avec l'ID donné depuis le stockage"""
    user = storage.get(User, user_id)
    # Si l'objet User n'est pas trouvé, retourne une erreur 404
    if user is None:
        abort(404)
    # Sérialise l'objet User en JSON et retourne la réponse
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def func_deleteuser(user_id):
    """Supprime un objet User"""
    # Récupère l'objet User avec l'ID donné depuis le stockage
    user = storage.get(User, user_id)
    # Si l'objet User n'est pas trouvé, retourne une erreur 404
    if user is None:
        abort(404)
    # Supprime l'objet User du stockage et enregistre les modifications
    storage.delete(user)
    storage.save()
    # Retourne une réponse vide avec le code d'état 200
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def func_createuser():
    """Crée un objet User"""
    # Récupère les données JSON de la requête
    datareq_json = request.get_json()
    # Si les données de la requête ne sont pas en JSON ou
    # la clé 'email' ou 'password' est manquante,
    # retourne une erreur 400
    if datareq_json is None:
        abort(400, "Not a JSON")
    if 'email' not in datareq_json:
        abort(400, "Missing email")
    if 'password' not in datareq_json:
        abort(400, "Missing password")
    # Crée un nouvel objet User avec les données de la requête
    nw_user = User(**datareq_json)
    # Enregistre le nouvel objet User dans le stockage
    nw_user.save()
    # Sérialise le nouvel objet User en JSON et retourne la réponse
    return jsonify(nw_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def func_updateuser(user_id):
    """Met à jour un objet User"""
    # Récupère l'objet User avec l'ID donné depuis le stockage
    user = storage.get(User, user_id)
    # Si l'objet User n'est pas trouvé, retourne une erreur 404
    if user is None:
        abort(404)
    # Récupère les données JSON de la requête
    datareq_json = request.get_json()
    # Si les données de la requête ne
    # sont pas en JSON, retourne une erreur 400
    if datareq_json is None:
        abort(400, "Not a JSON")
    # Liste des clés à ignorer lors de la mise à jour
    ignrkeys = ['id', 'email', 'created_at', 'updated_at']
    # Met à jour l'objet User avec les données de la requête
    for key, value in datareq_json.items():
        if key not in ignrkeys:
            setattr(user, key, value)
    # Enregistre l'objet User mis à jour dans le stockage
    user.save()
    # Sérialise l'objet User mis à jour
    # en JSON et retourne la réponse
    return jsonify(user.to_dict()), 200
