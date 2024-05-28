#!/usr/bin/python3
""" Module for user view """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from werkzeug.utils import secure_filename
import os
from flask import current_app as app


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Returns all users """
    
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    
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
    
    filename = None
    if 'profile_pic' in request.files:
        profile_pic = request.files['profile_pic']

        if profile_pic.filename != '':
            if not allowed_file(profile_pic.filename):
                abort(400, 'Invalid file type')
            filename = secure_filename(profile_pic.filename)
            upload_path = os.path.join("web_dynamic/static/uploads", filename)
            
            # Create directory if it does not exist
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
            # Save the file
            profile_pic.save(upload_path)
    
    data = request.form.to_dict()
    if filename:
        data['image'] = filename
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    user.save()
    
    return jsonify(user.to_dict()), 200

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
