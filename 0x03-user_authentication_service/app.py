#!/usr/bin/env python3
"""
Create a Flask app that has a single
GET route ("/") and use flask.jsonify to
return a JSON payload of the form:
"""

from flask import Flask, request, jsonify, make_response, abort
from flask import url_for, redirect
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    respond to the POST /sessions route.

    The request is expected to contain form data with "email"
    and a "password" fields.

    If the login information is incorrect, use flask.abort to
    respond with a 401 HTTP status.

    Otherwise, create a new session for the user, store it the
    session ID as a cookie with key "session_id" on the response
    and return a JSON payload of the form
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password) is False:
        abort(401)

    response = make_response(jsonify({
        "email": email,
        "message": "logged in"
        }))
    session_id = AUTH.create_session(email)
    response.set_cookie("sassion_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    respond to the DELETE /sessions route.

    The request is expected to contain the session ID as a cookie wit
    key "session_id".

    Find the user with the requested session ID. If the user exists
    destroy the session and redirect the user to GET /. If the user
    does not exist, respond with a 403 HTTP status.
    """

    session_id = request.cookies.get("session_id")
    if session_id is not None:
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect(url_for("home"))
    abort(403)


if __name__ == "__main__":
    app.run()
