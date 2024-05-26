#!/usr/bin/python3
""" Module for index.py """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.hosting_plan import HostingPlan
from models.user import User
from models.admin import Admin
from models.base_model import BaseModel
from models.billing_cycle import BillingCycle
from models.invoice import Invoice
from models.order import Order
from models.payment import Payment
from models.profile import Profile
from models.service import Service


@app_views.route("/status", strict_slashes=False)
def status() -> str:
    """ GET /status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats() -> str:
    """ GET /stats
    """
    return jsonify({
        "users": storage.count(User),
        "admins": storage.count(Admin),
        "hosting_plans": storage.count(HostingPlan),
        "billing_cycles": storage.count(BillingCycle),
        "invoices": storage.count(Invoice),
        "orders": storage.count(Order),
        "payments": storage.count(Payment),
        "profiles": storage.count(Profile),
        "services": storage.count(Service)
    })
