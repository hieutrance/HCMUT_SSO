from flask import Blueprint, request, jsonify
from http import HTTPStatus

test_bp = Blueprint("test", __name__)

@test_bp.get("/")
def teset():
    return jsonify({"status": "success", "msg": "HELLO WORD"}), HTTPStatus.ACCEPTED
