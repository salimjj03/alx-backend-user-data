#!/usr/bin/env python3
"""
Create a Flask app that has a single
GET route ("/") and use flask.jsonify to
return a JSON payload of the form:
"""

from flask import Flask, request, jsonify
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    return a JSON payload of the form
    """

    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    function that implements the POST /users route.
    """

    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify(
                {
                    "email": "{}".format(email),
                    "message": "user created"
                    }
                )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run()
