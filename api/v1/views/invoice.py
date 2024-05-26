#!/usr/bin/python3
""" Module for invoice view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.invoice import Invoice


@app_views.route('/invoices', methods=['GET'], strict_slashes=False)
def get_invoices():
    """ Returns all invoices """
    
    invoices = storage.all(Invoice).values()
    invoices = [invoice.to_dict() for invoice in invoices]
    
    return jsonify(invoices)


@app_views.route('/invoices/<invoice_id>', methods=['GET'], strict_slashes=False)
def get_invoice(invoice_id):
    """ Returns an invoice """
    
    invoice = storage.get(Invoice, invoice_id)
    if not invoice:
        abort(404)
        
    return jsonify(invoice.to_dict())


@app_views.route('/invoices/<invoice_id>', methods=['DELETE'], strict_slashes=False)
def delete_invoice(invoice_id):
    """ Deletes an invoice """
    
    invoice = storage.get(Invoice, invoice_id)
    if not invoice:
        abort(404)
        
    storage.delete(invoice)
    storage.save()
    
    return jsonify({}), 200


@app_views.route('/invoices', methods=['POST'], strict_slashes=False)
def post_invoice():
    """ Creates an invoice """
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'hosting_plan_id' not in data:
        abort(400, 'Missing hosting_plan_id')
    if 'order_id' not in data:
        abort(400, 'Missing order_id')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'amount_due' not in data:
        abort(400, 'Missing amount_due')
    if 'paid' not in data:
        abort(400, 'Missing paid')
    
    invoice = Invoice(**data)
    storage.new(invoice)
    storage.save()
    
    return jsonify(invoice.to_dict()), 201
