from flask import Blueprint, request, jsonify
from http import HTTPStatus
test_bp = Blueprint("test", __name__)

@test_bp.post("/test")
def test():
    return jsonify({
        "msg": "Hello World"
    }), HTTPStatus.ACCEPTED