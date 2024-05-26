#!/usr/bin/python3
""" Module for admin view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.admin import Admin


@app_views.route('/admins', methods=['GET'], strict_slashes=False)
def get_admins():
    """ Returns all admins """
    
    admins = storage.all(Admin).values()
    admins = [admin.to_dict() for admin in admins]
    
    return jsonify(admins)


@app_views.route('/admins/<admin_id>', methods=['GET'], strict_slashes=False)
def get_admin(admin_id):
    """ Returns an admin """
    
    admin = storage.get(Admin, admin_id)
    if not admin:
        abort(404)
        
    return jsonify(admin.to_dict())


@app_views.route('/admins/<admin_id>', methods=['DELETE'], strict_slashes=False)
def delete_admin(admin_id):
    """ Deletes an admin """
    
    admin = storage.get(Admin, admin_id)
    if not admin:
        abort(404)
        
    storage.delete(admin)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/admins', methods=['POST'], strict_slashes=False)
def post_admin():
    """ Creates an admin """
    
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
    
    admin = Admin(**data)
    admin.save()
    
    return jsonify(admin.to_dict()), 201


@app_views.route('/admins/<admin_id>', methods=['PUT'], strict_slashes=False)
def put_admin(admin_id):
    """ Updates an admin """
    
    admin = storage.get(Admin, admin_id)
    if not admin:
        abort(404)
        
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(admin, key, value)
    
    admin.save()
    
    return jsonify(admin.to_dict()), 200
