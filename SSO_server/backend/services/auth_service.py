from db import execute_sql
from utils.security import hash_password, verify_password, create_jwt
from http import HTTPStatus
from flask import jsonify

def register_user(data):
    username = data.get("username")
    password = data.get("password")
    fullname = data.get("fullname")
    email = data.get("email")
    phone = data.get("phone")

    user = execute_sql(
        "SELECT * FROM users WHERE username=%s",
        (username,),
        fetch_one=True
    )
    print(f"USER: {user}")
    if user:
        return jsonify({"status": "fail", "msg": "Existed username"}), HTTPStatus.BAD_REQUEST

    
    hashed = hash_password(password)
    new_user = execute_sql(
        "INSERT INTO users (username, password, fullname, email, phone) VALUES (%s,%s,%s,%s,%s)",
        (username, hashed, fullname, email, phone)
    )
    return jsonify({"status": "success", "msg": "Successully saved new user"}), HTTPStatus.CREATED

def login_user(data):
    username = data.get("username")
    password = data.get("password")
    user = execute_sql(
        "SELECT * FROM users WHERE username=%s", (username,),
        fetch_one=True
    )

    if not user or not verify_password(password, user["password"]):
        return None, "Invalid credentials"

    token = create_jwt({"user_id": user["id"]})
    return token, None
