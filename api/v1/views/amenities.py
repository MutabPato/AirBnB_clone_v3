#!/usr/bin/python3
"""
Create a new view for Amenity objects
that handles all default RESTFul API actions
"""


from flask import Flask, jsonify, request, abort
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_id(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new Amenity"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort(400, "Missing name")

    data = request.get_json()
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    storage.save()

    return jsonify(amenity.to_dict()), 200


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
