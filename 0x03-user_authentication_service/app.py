#!/usr/bin/env python3
"""
Flask app module to handle user registration.
"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

# Instantiate the Auth object
AUTH = Auth()

# Initialize Flask app
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """
    GET route that returns a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    Endpoint to register a new user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Handle POST requests to /sessions for user login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Missing email or password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({
            "email": email,
            "message": "logged in"
        })
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401, description="Invalid login credentials")


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
