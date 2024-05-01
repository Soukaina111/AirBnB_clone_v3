#!/usr/bin/python3
""" let's configure a flask app
"""

from flask import Flask, jsonify
from flask import abort, request
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

# Configuration CORS
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def Func_closestore(self):
    '''Ferme le stockage'''
    storage.close()


@app.errorhandler(404)
def sorry_page_not_found(error):
    """
    Gère les erreurs 404 en renvoyant une réponse JSON indiquant l'erreur.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True)
