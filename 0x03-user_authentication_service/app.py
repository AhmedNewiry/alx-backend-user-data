#!/usr/bin/env python3
"""
Flask app module to handle requests.
"""

from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Define route for "/"


@app.route("/", methods=["GET"])
def welcome():
    """
    GET route that returns a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    POST route to register a new user with email and password.

    Expects form data with "email" and "password" fields.
    """
    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        # Attempt to register the user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError as e:
        # Handle case where user already exists
        return jsonify({"message": str(e)}), 400


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
