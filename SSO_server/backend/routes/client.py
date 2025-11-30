from flask import Blueprint, request, jsonify
from services.client_service import register_client, login_client

client_bp = Blueprint("clients", __name__)

@client_bp.post("/register")
def register():
    return register_client(request)

@client_bp.post("/login")
def login():
    return login_client(request)