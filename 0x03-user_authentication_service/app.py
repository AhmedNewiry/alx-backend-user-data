#!/usr/bin/env python3
"""
Flask app module to handle user registration.
"""

from flask import Flask, jsonify, request
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


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
