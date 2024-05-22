#!/usr/bin/env python3
""" Module for siteswift.py
"""
from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SITESWIFT_SECRET_KEY')
app.config.update(SESSION_COOKIE_MAX_AGE=60)


@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    """
    return render_template('index.html')



if __name__ == "__main__":
    host = os.getenv('SITESWIFT_API_HOST')
    port = os.getenv('SITESWIFT_API_PORT')
    
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5001'
    
    app.run(host=host, port=port, debug=False)
