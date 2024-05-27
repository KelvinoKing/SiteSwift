#!/usr/bin/python3
""" Module for order view """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.order import Order


@app_views.route('/orders', methods=['GET'], strict_slashes=False)
def get_orders():
    """ Returns all orders """
    
    orders = storage.all(Order).values()
    orders = [order.to_dict() for order in orders]
    
    return jsonify(orders)


@app_views.route('/orders/<order_id>', methods=['GET'], strict_slashes=False)
def get_order(order_id):
    """ Returns an order """
    
    order = storage.get(Order, order_id)
    if not order:
        abort(404)
        
    return jsonify(order.to_dict())


@app_views.route('/orders/<order_id>', methods=['DELETE'], strict_slashes=False)
def delete_order(order_id):
    """ Deletes an order """
    
    order = storage.get(Order, order_id)
    if not order:
        abort(404)
        
    storage.delete(order)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/orders', methods=['POST'], strict_slashes=False)
def post_order():
    """ Creates an order """
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'hosting_plan_id' not in data:
        abort(400, 'Missing hosting_plan_id')
    if 'amount' not in data:
        abort(400, 'Missing amount_due')
    if 'status' not in data:
        abort(400, 'Missing order_status')
    
    order = Order(**data)
    order.save()
    
    return jsonify(order.to_dict()), 201


@app_views.route('/orders/<order_id>', methods=['PUT'], strict_slashes=False)
def put_order(order_id):
    """ Updates an order """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)
            
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
            
    for key, value in data.items():
        if key == 'status':
            setattr(order, key, value)
                
    order.save()

    # Return a success response
    return "Success", 200
