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

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

