#!/usr/bin/env python3
"""
Create a Flask app that has a single
GET route ("/") and use flask.jsonify to
return a JSON payload of the form:
"""

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    return a JSON payload of the form
    """

    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run()
