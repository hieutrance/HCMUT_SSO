import bcrypt
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

SECRET = os.getenv("JWT_SECRET_KEY")

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_jwt(payload):
    import datetime
    payload.update(
        {"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}
    )
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_jwt(token):
    try:
        # decode và verify exp tự động
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return True, payload
    except jwt.ExpiredSignatureError:
        # token hết hạn
        return False, "expired"
    except jwt.InvalidTokenError:
        # token không hợp lệ
        return False, "invalid"