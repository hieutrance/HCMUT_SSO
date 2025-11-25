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