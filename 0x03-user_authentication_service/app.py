#!/usr/bin/env python3
""" Flask Application Entry module """
from flask import Flask, abort, jsonify, request, make_response
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ user registration route handler """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """ sessions endpoint handler
        creates new session for user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    print("all valid credentials")
    session_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
