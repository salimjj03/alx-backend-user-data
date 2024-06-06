#!/usr/bin/env python3
"""
Flask view that handles all routes for the Session
authentication
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models.user import User
from os import getenv


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login():
    """
    login route
    """

    dic = request.form
    if "email" not in dic or dic.get("email") is None:
        return jsonify({"error": "email missing"}), 400

    if "password" not in dic or dic.get("password") is None:
        return jsonify({"error": "password missing"}), 400

    user_name = dic.get("email")
    passwd = dic.get("password")

    user = User.search({"email": user_name})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(passwd) is False:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    user_dic = jsonify(user[0].to_json())
    user_dic.set_cookie(getenv("SESSION_NAME"), session_id)
    return user_dic

@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False)
def logout():
    """
    delete session
    """

    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
