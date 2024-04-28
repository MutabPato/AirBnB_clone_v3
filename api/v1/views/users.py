#!/usr/bin/python3
"""
Create a new view for User objects
that handles all default RESTFul API actions
"""


from flask import Flask, jsonify, request, abort
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route(
        '/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_id(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User"""
    if not request.get_json():
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort(400, "Missing name")

    data = request.get_json()
    user = User(**data)
    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


@app_views.route(
        '/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    data = request.get_json()

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict()), 200


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
