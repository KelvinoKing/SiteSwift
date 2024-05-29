#!/usr/bin/python3
""" Module for billing cycle view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.billing_cycle import BillingCycle


@app_views.route('/billing_cycles', methods=['GET'], strict_slashes=False)
def get_billing_cycles():
    """ Returns all billing cycles """
    
    billing_cycles = storage.all(BillingCycle).values()
    billing_cycles = [billing_cycle.to_dict() for billing_cycle in billing_cycles]
    
    return jsonify(billing_cycles)


@app_views.route('/billing_cycles/<billing_cycle_id>', methods=['GET'], strict_slashes=False)
def get_billing_cycle(billing_cycle_id):
    """ Returns a billing cycle """
    
    billing_cycle = storage.get(BillingCycle, billing_cycle_id)
    if not billing_cycle:
        abort(404)
        
    return jsonify(billing_cycle.to_dict())


@app_views.route('/billing_cycles/<billing_cycle_id>', methods=['DELETE'], strict_slashes=False)
def delete_billing_cycle(billing_cycle_id):
    """ Deletes a billing cycle """
    
    billing_cycle = storage.get(BillingCycle, billing_cycle_id)
    if not billing_cycle:
        abort(404)
        
    storage.delete(billing_cycle)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/billing_cycles', methods=['POST'], strict_slashes=False)
def post_billing_cycle():
    """ Creates a billing cycle """
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'hosting_plan_id' not in data:
        abort(400, 'Missing hosting_plan_id')
    if 'order_id' not in data:
        abort(400, 'Missing order_id')
    if 'cycle_start' not in data:
        abort(400, 'Missing cycle_start')
    if 'cycle_end' not in data:
        abort(400, 'Missing cycle_end')
    if 'amount_due' not in data:
        abort(400, 'Missing amount_due')
    if 'payment_date' not in data:
        abort(400, 'Missing payment_date')
    
    billing_cycle = BillingCycle(**data)
    billing_cycle.save()
    
    return jsonify(billing_cycle.to_dict()), 201


@app_views.route('/billing_cycles/<billing_cycle_id>', methods=['PUT'], strict_slashes=False)
def put_billing_cycle(billing_cycle_id):
    """ Updates a billing cycle """
    
    billing_cycle = storage.get(BillingCycle, billing_cycle_id)
    if not billing_cycle:
        abort(404)
        
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(billing_cycle, key, value)
    
    storage.save()
    
    return jsonify(billing_cycle.to_dict()), 200
