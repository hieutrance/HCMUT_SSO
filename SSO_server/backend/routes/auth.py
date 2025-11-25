from flask import Blueprint, request, jsonify
from services.auth_service import register_user, authorization, exchange_token, check_token_expiration, get_user_info

from http import HTTPStatus

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/test")
def test():
    return "Hello World", HTTPStatus.OK

@auth_bp.post("/register")
def register():
    return register_user(request)
    
@auth_bp.post("/authenticate")
def login():
    return authorization(request)

@auth_bp.post("/token")
def post_exchange_token():
    return exchange_token(request)

@auth_bp.get("/user-info")
def user_info():
    return get_user_info(request)