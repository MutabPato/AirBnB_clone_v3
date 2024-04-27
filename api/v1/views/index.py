#!/usr/bin/python3
"""


"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    return jsonify({
        "status": "OK"
        })


@app_views.route('/stats', methods=['GET'])
def stats():
    objects_count = {
        "amenities": storage.count('Amenities'),
        "cities": storage.count('Cities'),
        "places": storage.count('Places'),
        "reviews": storage.count('Reviews'),
        "states": storage.count('States'),
        "users": storage.count('Users'),
        }

    return jsonify(objects_count)
