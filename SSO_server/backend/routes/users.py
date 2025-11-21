from flask import Blueprint, request, jsonify
from services.user_service import register_user, login_user

users_bp = Blueprint("users", __name__)

@users_bp.post("/register")
def register():
    data = request.json
    result, err = register_user(data)
    if err:
        return jsonify({"status": "error", "message": err}), 400
    return jsonify({"status": "success", "user_id": result})

@users_bp.post("/login")
def login():
    data = request.json
    token, err = login_user(data)
    if err:
        return jsonify({"status": "error", "message": err}), 401
    return jsonify({"status": "success", "access_token": token})
