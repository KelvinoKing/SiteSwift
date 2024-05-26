#!/usr/bin/python3
""" Module for profile view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.profile import Profile


@app_views.route('/profiles', methods=['GET'], strict_slashes=False)
def get_profiles():
    """ Returns all profiles """
    
    profiles = storage.all(Profile).values()
    profiles = [profile.to_dict() for profile in profiles]
    
    return jsonify(profiles)


@app_views.route('/profiles/<profile_id>', methods=['GET'], strict_slashes=False)
def get_profile(profile_id):
    """ Returns a profile """
    
    profile = storage.get(Profile, profile_id)
    if not profile:
        abort(404)
        
    return jsonify(profile.to_dict())


@app_views.route('/profiles/<profile_id>', methods=['DELETE'], strict_slashes=False)
def delete_profile(profile_id):
    """ Deletes a profile """
    
    profile = storage.get(Profile, profile_id)
    if not profile:
        abort(404)
        
    storage.delete(profile)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/profiles', methods=['POST'], strict_slashes=False)
def post_profile():
    """ Creates a profile """
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'first_name' not in data:
        abort(400, 'Missing first_name')
    if 'last_name' not in data:
        abort(400, 'Missing last_name')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'phone' not in data:
        abort(400, 'Missing phone')
    if 'profile_pic' not in data:
        abort(400, 'Missing profile_picture')

    profile = Profile(**data)
    profile.save()
    
    return jsonify(profile.to_dict()), 201


@app_views.route('/profiles/<profile_id>', methods=['PUT'], strict_slashes=False)
def put_profile(profile_id):
    """ Updates a profile """
    
    profile = storage.get(Profile, profile_id)
    if not profile:
        abort(404)
        
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    for key, value in data.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(profile, key, value)
    
    profile.save()
    
    return jsonify(profile.to_dict()), 200
