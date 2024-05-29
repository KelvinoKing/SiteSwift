#!/usr/bin/env python3
""" Module for siteswift.py
"""
from flask import Flask, render_template, jsonify, abort, redirect, Response
import os
from dotenv import load_dotenv
import requests
from auth import Auth
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Dict, Union, Any, Tuple
from flask import flash
import uuid


load_dotenv()

Auth = Auth()
app = Flask(__name__)
app.secret_key = "SITESWIFT_SECRET"
app.config.update(SESSION_COOKIE_MAX_AGE=60)


@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
def index() -> str:
    """ GET /
    """
    url = "http://localhost:5000/api/v1/hosting_plans"
    hosting_plan = requests.get(url).json()

    cached_id=str(uuid.uuid4())
    
    return render_template('index.html', hosting_plan=hosting_plan, cached_id=cached_id)


@app.route("/register", methods=['GET'], strict_slashes=False)
def register() -> str:
    """ GET /register
    """
    cached_id = str(uuid.uuid4())
    return render_template('signup.html', cached_id=cached_id)


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> Union[str, Tuple[str, int]]:
    """ POST /register
    """
    user_json = request.get_json()
    if not user_json:
        return ('Missing JSON', 400)
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')
    if 'first_name' not in user_json:
        abort(400, 'Missing first_name')
    if 'last_name' not in user_json:
        abort(400, 'Missing last_name')
    
    email = user_json.get('email')
    password = user_json.get('password')
    first_name = user_json.get('first_name')
    last_name = user_json.get('last_name')

    try:
        Auth.register_user(first_name, last_name, email, password)
        flash('User created successfully. Kindly login to continue.')
        return redirect('/register')
    except ValueError:
        return jsonify('User {} already exists'.format(email), 400)
    

@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> Union[str, Tuple[str, int]]:
    """ POST /login
    """

    user_json = request.get_json()
    if not user_json:
        return ('Missing JSON', 400)
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')

    email = user_json.get('email')
    password = user_json.get('password')
    
    if not Auth.valid_login(email, password):
        return ('Invalid email or password', 401)
    session_id = Auth.create_session(email)
    if not session_id:
        abort(401)
    resp = Response('Success')
    resp.set_cookie('session_id', session_id)
    return resp


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /logout
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    Auth.destroy_session(user.id)
    return redirect('/')
    

@app.route("/account", methods=['GET'], strict_slashes=False)
def account() -> str:
    """ GET /account
    """
    session_id = request.cookies.get('session_id')
    user1 = Auth.get_user_from_session_id(session_id)
    if not user1:
        flash('Please login to continue.')
        return redirect('/register')
    url = "http://localhost:5000/api/v1/orders"
    orders = requests.get(url).json()
    user_orders = []
    for order in orders:
        if order['user_id'] == user1.id:
            user_orders.append(order)

    url2 = "http://localhost:5000/api/v1/hosting_plans"
    hosting_plans = requests.get(url2).json()

    # Sort orders by date
    user_orders = sorted(user_orders, key=lambda x: x['created_at'], reverse=True)

    user_api_url = "http://localhost:5000/api/v1/users/{}".format(user1.id)
    user = requests.get(user_api_url).json()
    
    flash('Welcome back, {}'.format(user1.first_name))
    cached_id = str(uuid.uuid4())
    return render_template('myaccount.html', user=user, orders=user_orders, hosting_plans=hosting_plans, cached_id=cached_id)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        flash('Please login to continue.')
        return redirect('/register')
    flash('Welcome back, {}'.format(user.first_name))
    cached_id = str(uuid.uuid4())
    return render_template('profile.html', user=user, cached_id=cached_id)


@app.route("/reset_password", methods=['GET'], strict_slashes=False)
def reset_password() -> str:
    """ GET /reset_password
    """

    cached_id = str(uuid.uuid4())
    return render_template('forgot-password.html', cached_id=cached_id)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def update_password() -> str:
    """ POST /reset_password
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Auth._db.find_user_by(email=email)
    if not user:
        return "User not found."

    reset_token = Auth.get_reset_password_token(email)
    try:
        Auth.update_password(reset_token, password)
    except ValueError:
        return "Invalid reset token."
    return redirect('/register')
    

@app.route("/update_profile", methods=['POST'], strict_slashes=False)
def update_profile() -> str:
    """ POST /update_profile
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        flash('Please login to continue.')
        return redirect('/register')
    user_json = request.get_json()
    if not user_json:
        return ('Missing JSON', 400)
    
    Auth.update_user(user.id, **user_json)
    flash('Profile updated successfully')
    return redirect('/profile')


@app.route("/services", methods=['GET'], strict_slashes=False)
def services() -> str:
    """ GET /services
    """

    url = "http://localhost:5000/api/v1/hosting_plans"
    hosting_plan = requests.get(url).json()

    cached_id=str(uuid.uuid4())
    
    return render_template('services.html', hosting_plan=hosting_plan, cached_id=cached_id)


@app.route("/order/<hosting_plan_id>", methods=['GET'], strict_slashes=False)
def order(hosting_plan_id) -> str:
    """ GET /order
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        flash('Please login to continue.')
        return redirect('/register')
    url1 = "http://localhost:5000/api/v1/hosting_plans/{}".format(hosting_plan_id)
    hosting_plan = requests.get(url1).json()

    # Create order
    url2 = "http://localhost:5000/api/v1/orders"
    data = {
        "user_id": user.id,
        "hosting_plan_id": hosting_plan_id,
        "amount": hosting_plan['price'],
        "status": "pending"
    }
    order = requests.post(url2, json=data).json()
    cached_id=str(uuid.uuid4())
    return render_template('checkout.html', order_id=order['id'], cached_id=cached_id)


@app.route("/team", methods=['GET'], strict_slashes=False)
def team() -> str:
    """ GET /team
    """
    cached_id=str(uuid.uuid4())
    return render_template('team.html', cached_id=cached_id)


@app.route("/about", methods=['GET'], strict_slashes=False)
def about() -> str:
    """ GET /about
    """
    cached_id=str(uuid.uuid4())
    return render_template('about.html', cached_id=cached_id)


@app.route("/blog", methods=['GET'], strict_slashes=False)
def blog() -> str:
    """ GET /blog
    """
    cached_id=str(uuid.uuid4())
    return render_template('blog.html', cached_id=cached_id)


@app.route("/admin", methods=['GET'], strict_slashes=False)
def admin() -> str:
    """ GET /admin
    """
    cached_id=str(uuid.uuid4())
    return render_template('admin-signup.html', cached_id=cached_id)


@app.route("/admin/sessions", methods=['POST'], strict_slashes=False)
def admin_login() -> Union[str, Tuple[str, int]]:
    """ POST /login
    """

    user_json = request.get_json()
    if not user_json:
        return ('Missing JSON', 400)
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')

    email = user_json.get('email')
    password = user_json.get('password')
    
    if not Auth.valid_admin_login(email, password):
        return ('Invalid email or password', 401)
    session_id = Auth.create_admin_session(email)
    if not session_id:
        abort(401)
    resp = Response('Success')
    resp.set_cookie('session_id', session_id)
    return resp


@app.route("/admin/sessions", methods=['DELETE'], strict_slashes=False)
def admin_logout() -> str:
    """ DELETE /logout
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_admin_from_session_id(session_id)
    if not user:
        abort(403)
    Auth.destroy_admin_session(user.id)
    return "Success"


@app.route("/admin/account", methods=['GET'], strict_slashes=False)
def admin_account() -> str:
    """ GET /account
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_admin_from_session_id(session_id)
    if not user:
        flash('Please login to continue.')
        return redirect('/admin')
    flash('Welcome back, {}'.format(user.first_name))
    
    url = "http://localhost:5000/api/v1/stats"
    stats = requests.get(url).json()
    cached_id=str(uuid.uuid4())
    return render_template('admin-dashboard.html', user=user, stats=stats, cached_id=cached_id)


@app.route("/admin/account/dashboard", methods=['GET'], strict_slashes=False)
def admin_dashboard() -> str:
    """ GET /account/dashboard
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_admin_from_session_id(session_id)
    if not user:
        return redirect('/admin')
    
    url = "http://localhost:5000/api/v1/stats"
    stats = requests.get(url).json()
    cached_id=str(uuid.uuid4())
    return render_template('admin-dashboard.html', user=user, stats=stats, cached_id=cached_id)


@app.route("/admin/account/customers", methods=['GET'], strict_slashes=False)
def admin_customers() -> str:
    """ GET /account/customers
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_admin_from_session_id(session_id)
    if not user:
        return redirect('/admin')
    
    url = "http://localhost:5000/api/v1/users"
    users = requests.get(url).json()
    cached_id=str(uuid.uuid4())
    return render_template('admin-customers.html', user=user, users=users, cached_id=cached_id)


@app.route("/admin/account/sales", methods=['GET'], strict_slashes=False)
def admin_sales() -> str:
    """ GET /account/sales
    """
    session_id = request.cookies.get('session_id')
    user = Auth.get_admin_from_session_id(session_id)
    if not user:
        return redirect('/admin')
    url = "http://localhost:5000/api/v1/orders"
    orders = requests.get(url).json()
    url2 = "http://localhost:5000/api/v1/hosting_plans"
    hosting_plans = requests.get(url2).json()
    url3 = "http://localhost:5000/api/v1/users"
    users = requests.get(url3).json()
    cached_id=str(uuid.uuid4())
    return render_template('admin-sales.html', user=user, orders=orders, hosting_plans=hosting_plans, users=users, cached_id=cached_id)



if __name__ == "__main__":
    host = os.getenv('SITESWIFT_API_HOST')
    port = os.getenv('SITESWIFT_API_PORT')
    
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5001'
    
    app.run(host=host, port=port, debug=True)
