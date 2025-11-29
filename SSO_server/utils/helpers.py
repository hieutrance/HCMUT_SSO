import secrets
import string
import time
import hmac
import hashlib
import datetime
import jwt
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from flask import jsonify
from db import execute_sql


SECRET = os.getenv("JWT_SECRET_KEY")

def create_jwt(payload: dict, expire_minutes: int = 10):
    """
    Tạo JWT với payload tùy chọn và thời gian hết hạn.
    """
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes)
    final_payload = {**payload, "exp": exp}

    token = jwt.encode(final_payload, SECRET, algorithm="HS256")
    return token

def verify_jwt(token, key, algorithm):
    try:
        # decode và verify exp tự động
        payload = jwt.decode(token, key, algorithms=[algorithm])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, "expired"
    except jwt.InvalidTokenError:
        return False, "invalid"
    
## ID_token exp_time: 10 mín
def generate_id_token(user_id, client_id):
    payload = {
        "iss": "http://localhost:8000",
        "sub": user_id,          
        "aud": client_id,        
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp())
    }

    # Đọc private key
    with open("D:\CODE_SPACE\SSO\HCMUT_SSO\private.pem", "r") as f:
        private_key = f.read()

    # Ký token bằng RSA-SHA256
    token = jwt.encode(payload, private_key, algorithm="RS256")

    return token

def get_client_id_from_jwt(token):
    try:
        # decode payload mà không verify signature
        payload = jwt.decode(token, options={"verify_signature": False})
        client_id = payload.get("iss")
        if not client_id:
            return None, "missing iss claim"
        return client_id, None
    except jwt.exceptions.InvalidTokenError:
        return None, "invalid token format"
    except Exception as e:
        return None, f"unexpected error: {str(e)}"


def validate_client_assertion(client_assertion_type: str, client_assertion: str):
    if not client_assertion:
        return jsonify({
            "error": "unauthorized",
            "error_description": "Unauthorized"
        }), HTTPStatus.UNAUTHORIZED

    if not client_assertion_type or client_assertion_type != "urn:ietf:params:oauth:client-assertion-type:jwt-bearer":
        return jsonify({
            "error": "unauthorized",
            "error_description": "unsupported_assertion_type"
        }), HTTPStatus.BAD_REQUEST
    
    client_id, error_msg = get_client_id_from_jwt(client_assertion)
    
    if client_id is None:
        return jsonify({
            "error": "unauthorized",
            "error_description": error_msg
        }), HTTPStatus.UNAUTHORIZED
        
    temp = execute_sql(''' 
                    SELECT secretKey FROM clients
                    WHERE id=%s                
                ''', (client_id,), True)
    client_secret = temp["secretKey"]
    print(f"Client secret's key: {client_secret}")
    print(f"Client_assertion: {client_assertion}")

    
    try: 
        payload = jwt.decode(client_assertion, client_secret, algorithms=["HS256"], audience="http://localhost:5000/token")
        print(f"Payload: {payload}")
        return True, payload
    except jwt.ExpiredSignatureError:
        return jsonify({
            "error": "unauthorized",
            "error_description": "Expired assertion"
        }), HTTPStatus.UNAUTHORIZED
    except jwt.InvalidTokenError:
        return jsonify({
            "error": "invalid_assertion",
            "error_description": "Invalid assertion"
        }), HTTPStatus.BAD_REQUEST
        
        
def is_valid_exp(exp: datetime):
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    else:
        exp = exp.astimezone(timezone.utc)

    now = datetime.now(timezone.utc)

    return exp > now

def generate_access_token(user_id, client_id):
    access_token = secrets.token_urlsafe(32)
    access_token_exp = (datetime.now(timezone.utc) + timedelta(minutes=10)).replace(tzinfo=None)
    check = execute_sql("""
            INSERT INTO access_tokens(token, client_id, user_id, scope, expires_at, revoked) 
            VALUES(%s,%s,%s,%s,%s,%s)
            """,
            (access_token, client_id, user_id, "openid profile", access_token_exp, False)
            )
   
    if not check:
        return False, jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    
    return True, access_token, access_token_exp

def generate_refresh_token(user_id, client_id): 
    refresh_token = secrets.token_urlsafe(32)
    refresh_token_exp = (datetime.now(timezone.utc) + timedelta(days=1)).replace(tzinfo=None)
    
    check = execute_sql("""
        INSERT INTO refresh_tokens(token, client_id, user_id, expires_at, revoked)
        VALUES(%s,%s,%s,%s,%s)             
        """,
        (refresh_token, client_id, user_id, refresh_token_exp, False)
        )
    
    if not check:
        return False, jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
        
    return True, refresh_token, refresh_token_exp
