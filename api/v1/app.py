#!/usr/bin/python3
""" Module for app.py """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": ["http://127.0.0.1:5001", "http://127.0.0.1:5000"]}}, supports_credentials=True)


@app.teardown_appcontext
def close_db(error):
    """ Closes the database again at the end of the request. """
    storage.close()
    

@app.errorhandler(404) 
def error_handlers(error):
    """ Error handler """
    print(error)
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host = environ.get('SITESWIFT_API_HOST')
    port = environ.get('SITESWIFT_API_PORT')
    
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
        
    app.run(host=host, port=port, debug=True)
