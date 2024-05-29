#!/usr/bin/python3
""" Module for payment view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.payment import Payment


@app_views.route('/payments', methods=['GET'], strict_slashes=False)
def get_payments():
    """ Returns all payments """
    
    payments = storage.all(Payment).values()
    payments = [payment.to_dict() for payment in payments]
    
    return jsonify(payments)


@app_views.route('/payments/<payment_id>', methods=['GET'], strict_slashes=False)
def get_payment(payment_id):
    """ Returns a payment """
    
    payment = storage.get(Payment, payment_id)
    if not payment:
        abort(404)
        
    return jsonify(payment.to_dict())


@app_views.route('/payments/<payment_id>', methods=['DELETE'], strict_slashes=False)
def delete_payment(payment_id):
    """ Deletes a payment """
    
    payment = storage.get(Payment, payment_id)
    if not payment:
        abort(404)
        
    storage.delete(payment)
    storage.save()
    
    return jsonify({}), 200
