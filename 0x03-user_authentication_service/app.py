#!/usr/bin/env python3
"""
Flask app module to handle user registration.
"""

from flask import Flask, jsonify, request, abort, make_response, redirect
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


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    POST /users route to register a new user.
    Expects two form fields: 'email' and 'password'.
    """
    # Get email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        # Register the user using Auth
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout route that destroys the user session if it exists."""
    # Get session_id from cookies
    session_id = request.cookies.get('session_id')

    # Find user by session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # If user exists, destroy session and redirect to /
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        # If no user is found, return 403 Forbidden
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Profile route that returns the user's email if the session is valid."""
    # Get session_id from cookies
    session_id = request.cookies.get('session_id')

    # Find user by session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # If user is found, return the user's email
        return jsonify({"email": user.email}), 200
    else:
        # If session_id is invalid or user does not exist, return 403
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    POST /reset_password route to get a reset password token.
    """
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
