from flask import Blueprint, request, jsonify
from http import HTTPStatus

openid_bp = Blueprint("openid", __name__)

@openid_bp.get("/authorization")
def authorization():
    pass

@openid_bp.post("/authorization")
def post_authorization():
    pass

@openid_bp.post("/token")
def exchange_token():
    pass

@openid_bp.post("/get-info")
def get_user_info():
    pass

openid_bp.get("/test")
def test():
    return "Hi"