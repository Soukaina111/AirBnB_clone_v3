#!/usr/bin/python3
"""initialise le package"""

from flask import Blueprint

# Importer les modules de niveau supérieur au début du fichier
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.amenities import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')²
