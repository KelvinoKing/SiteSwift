#!/usr/bin/python3

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.user import *
from api.v1.views.hosting_plan import *
from api.v1.views.admin import *
from api.v1.views.billing_cycles import *
from api.v1.views.invoice import *
from api.v1.views.orders import *
from api.v1.views.payment import *
from api.v1.views.profile import *
