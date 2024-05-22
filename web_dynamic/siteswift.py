#!/usr/bin/env python3
""" Module for siteswift.py
"""
from flask import Flask, render_template, jsonify, abort, redirect, Response
import os
from dotenv import load_dotenv
from auth import Auth
from flask import request
from sqlalchemy.orm.exc import NoResultFound
from typing import List, Dict, Union, Any, Tuple
from flask import flash


load_dotenv()

Auth = Auth()
app = Flask(__name__)
app.secret_key = os.getenv('SITESWIFT_API_SECRET_KEY')
app.config.update(SESSION_COOKIE_MAX_AGE=60)


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    """
    return render_template('index.html')


@app.route("/register", methods=['GET'], strict_slashes=False)
def register() -> str:
    """ GET /register
    """
    return render_template('signup.html')


@app.route("/signup", methods=['GET', 'POST'], strict_slashes=False)
def signup() -> Union[str, Tuple[str, int]]:
    """ POST /register
    """
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        Auth.register_user(first_name, last_name, email, password)
        return redirect('/login')
    except ValueError:
        return ('User {} already exists'.format(email), 400)
    

@app.route("/login", methods=['POST'], strict_slashes=False)
def login() -> Union[str, Tuple[str, int]]:
    """ POST /login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        if Auth.valid_login(email, password):
            return redirect('/profile')
        else:
            flash('Invalid login')
            return redirect('/login')
    except NoResultFound:
        return ('Invalid login', 401)
    

@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    """
    return render_template('profile.html')



if __name__ == "__main__":
    host = os.getenv('SITESWIFT_API_HOST')
    port = os.getenv('SITESWIFT_API_PORT')
    
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5001'
    
    app.run(host=host, port=port, debug=False)
