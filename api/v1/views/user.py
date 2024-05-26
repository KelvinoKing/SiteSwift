#!/usr/bin/python3
""" Module for user view """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Returns all users """
    
    print('Getting users')
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    print(users)
    
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Returns a user """
    
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user """
    
    user = storage.get(User, user_id)
    if not user:
        abort(404)
        
    storage.delete(user)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates a user """
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'first_name' not in data:
        abort(400, 'Missing first_name')
    if 'last_name' not in data:
        abort(400, 'Missing last_name')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password_hash' not in data:
        abort(400, 'Missing password')
    
    user = User(**data)
    user.save()
    
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Updates a user """
    
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    user.save()
    
    return jsonify(user.to_dict()), 200
