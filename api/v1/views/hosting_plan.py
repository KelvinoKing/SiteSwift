#!/usr/bin/python3
""" Module for hosting plan view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.hosting_plan import HostingPlan


@app_views.route('/hosting_plans', methods=['GET'], strict_slashes=False)
def get_hosting_plans():
    """ Returns all hosting plans """
    
    hosting_plans = storage.all(HostingPlan).values()
    hosting_plans = [hosting_plan.to_dict() for hosting_plan in hosting_plans]
    
    return jsonify(hosting_plans)


@app_views.route('/hosting_plans/<hosting_plan_id>', methods=['GET'], strict_slashes=False)
def get_hosting_plan(hosting_plan_id):
    """ Returns a hosting plan """
    
    hosting_plan = storage.get(HostingPlan, hosting_plan_id)
    if not hosting_plan:
        abort(404)
        
    return jsonify(hosting_plan.to_dict())


@app_views.route('/hosting_plans/<hosting_plan_id>', methods=['DELETE'], strict_slashes=False)
def delete_hosting_plan(hosting_plan_id):
    """ Deletes a hosting plan """
    
    hosting_plan = storage.get(HostingPlan, hosting_plan_id)
    if not hosting_plan:
        abort(404)
        
    storage.delete(hosting_plan)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/hosting_plans', methods=['POST'], strict_slashes=False)
def post_hosting_plan():
    """ Creates a hosting plan """
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'price' not in data:
        abort(400, 'Missing price')
    if 'description' not in data:
        abort(400, 'Missing description')
    if 'max_websites' not in data:
        abort(400, 'Missing max_websites')
    if 'max_space' not in data:
        abort(400, 'Missing max_space')
    if 'max_bandwidth' not in data:
        abort(400, 'Missing max_bandwidth')
    if 'max_email' not in data:
        abort(400, 'Missing max_email')
    if 'max_databases' not in data:
        abort(400, 'Missing max_databases')
    
    hosting_plan = HostingPlan(**data)
    storage.new(hosting_plan)
    storage.save()
    
    return jsonify(hosting_plan.to_dict()), 201


@app_views.route('/hosting_plans/<hosting_plan_id>', methods=['PUT'], strict_slashes=False)
def put_hosting_plan(hosting_plan_id):
    """ Updates a hosting plan """
    
    hosting_plan = storage.get(HostingPlan, hosting_plan_id)
    if not hosting_plan:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(hosting_plan, key, value)
    
    storage.save()
    
    return jsonify(hosting_plan.to_dict())
