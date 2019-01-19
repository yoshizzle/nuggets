import time
import logging

from configparser import ConfigParser
from datetime import datetime

from flask import Flask
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect, CSRFError

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# init our Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

config = ConfigParser()
config.readfp(open('config.ini'))
env = config.get('meta', 'environment')

_cfg = lambda k: config.get(env, k)
_cfgi = lambda k: int(_cfg(k))

# app.config['DEBUG'] = _cfgb('debug', default=False)
app.config['SECRET_KEY'] = _cfg('secret-key')
app.config['MONGO_URI'] = _cfg('db-uri')

mongo = PyMongo(app)
csrf = CSRFProtect()

# init blueprints
from nuggets import blueprints

import os
from flask import send_from_directory

# universal routes
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/favicon.ico')
def send_favicon():
    """
    Returns the favicon file from /static
    """
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<filename>.css')
def serve_css(filename):
    """
    Returns static css files from /static/css
    """
    return send_from_directory(os.path.join(app.root_path, 'static', 'css'),
                               '{}.css'.format(filename),
                               mimetype='text/css')


@app.route('/images/thumbnails/<image>')
def serve_static_images(image):
    """
    Returns an image from the images directory
    """
    return send_from_directory(os.path.join(app.config['IMAGE_DIR'], 'thumbnails'),
                               image)


# global decorators for the app
# @app.after_request
# def teardown(resp):
#     """
#     Ensure db session are safe across requests, and automatically rollback any
#     uncommitted changes.
#    """

from flask import request
@app.after_request
def apply_headers(response):
    # Useful-looking headers we don't have yet:
    #   - X-RateLimit-Limit
    #   - X-RateLimit-Remaining
    #   - X-RateLimit-Reset
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "HEAD, GET, OPTIONS, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Origin, X-Requested-With, Content-Type, Accept, X-Filter"

    # POST/DELETE/PUT are not cached unless explicitly done so
    if request.method == 'GET':
        response.headers["Vary"] = "Authorization, X-Filter"

    return response
