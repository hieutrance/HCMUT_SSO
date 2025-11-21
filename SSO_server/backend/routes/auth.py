from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
from http import HTTPStatus

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/test")
def test():
    return "Hello World", HTTPStatus.OK

@auth_bp.post("/register")
def register():
    data = request.json
    return register_user(data)
    
@auth_bp.post("/login")
def login():
    data = request.json
    token, err = login_user(data)
    if err:
        return jsonify({"status": "error", "message": err}), 401
    return jsonify({"status": "success", "access_token": token})
