from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user
from http import HTTPStatus

test_bp = Blueprint("test", __name__)

@test_bp.get("/")
def teset():
    return jsonify({"status": "success", "msg": "HELLO WORD"}), HTTPStatus.ACCEPTED
