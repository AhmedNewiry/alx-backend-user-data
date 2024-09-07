#!/usr/bin/env python3
""" Session authentication views """
from flask import Blueprint, request, jsonify
from models.user import User
import os

# Create a blueprint for session authentication routes
session_auth_bp = Blueprint('session_auth', __name__, url_prefix='/api/v1')


@session_auth_bp.route('/auth_session/login/', methods=['POST'])
def login():
    """ Handle login requests """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth to avoid circular import
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
