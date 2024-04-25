#!/usr/bin/env python3
""" Session auth views module j:qa
"""
from os import getenv
from werkzeug.wrappers import auth
from models.user import User
from api.v1.views import app_views
from flask import jsonify, make_response, request


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles login endpoint
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"})
    user_list = User.search({'email': email})
    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_list[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = make_response(user.to_json())
    resp.set_cookie(getenv('SESSION_NAME'), session_id)
    return resp
