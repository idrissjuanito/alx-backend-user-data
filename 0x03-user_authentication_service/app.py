#!/usr/bin/env python3
""" Flask Application Entry module """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
