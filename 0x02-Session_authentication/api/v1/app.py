#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth variable
auth = None

# Load authentication based on environment variable
auth_type = os.getenv('AUTH_TYPE')
if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
else:
    if auth_type == 'auth':
        auth = Auth()


@app.before_request
def before_request():
    """Function to run before each request."""
    if auth is None:
        return
    request.current_user = auth.current_user(request)
    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
    ]
    # Check if the path requires authentication
    if auth.require_auth(request.path, excluded_paths):
        # Check for the authorization header
        if (auth.authorization_header(request) is None
                and auth.session_cookie(request) is None):
            abort(401, description="Unauthorized")
        # Check for the current user
        if auth.current_user(request) is None:
            abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error):
    """unauthorized error handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error):
    """Forbidden error handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
