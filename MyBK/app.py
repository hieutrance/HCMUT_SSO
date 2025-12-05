import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, session, request
import base64, secrets
from datetime import datetime, timezone, timedelta
import time, jwt
import uuid

import requests
load_dotenv()
from db import get_connection

SERVICE_PORT = 3000 
SERVICE_URL = f"http://localhost:{SERVICE_PORT}"
SSO_SERVER_URL = "http://localhost:5000" 
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_TOKEN = os.getenv("API_TOKEN")

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
@app.route('/home')
def home_page():
    user_info = {
        'username': session.get('username', 'Khách'),
        'is_logged_in': session.get('is_logged_in', False)
    }
    return render_template('Homepage.html', **user_info)


@app.route('/dashboard')
def mybk_dashboard():
    print(f"VALUE OF is_logged_in {session.get('is_logged_in')}")
    if not session.get('is_logged_in'):
        return redirect(url_for('login_page'))
    
    return render_template('Mybk.html', username=session.get('username'))


@app.route('/login')
def login_page():
    callback_url = f"{SERVICE_URL}/sso-callback"
    sso_redirect_url = (
        f"{SSO_SERVER_URL}/authorize?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={callback_url}&"
        f"response_type=code&"
        f"scope='openid profile email'"
    )
    
    return redirect(sso_redirect_url)


@app.route('/sso-callback')
def sso_callback():
    auth_code = request.args.get('code')
    
    if auth_code:
        payload = {
            "iss": CLIENT_ID,
            "sub": CLIENT_ID,
            "aud": 'http://localhost:5000/token',
            "exp": int(time.time()) + 300  # 5 phút
        }
        client_assertion = jwt.encode(payload, CLIENT_SECRET, algorithm="HS256")
        response = requests.post(
            API_TOKEN,
            json={
                "grant_type": "code",
                "code": auth_code,
                "redirect_uri": f"{SERVICE_URL}/sso-callback",
                "scope": "profile email",
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                "client_assertion": client_assertion
            }
        )

        ## ERROR HANDLE
        if response.status_code != 200:
            data = {}
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                print(f"Lỗi: Response từ Token Endpoint không phải JSON. Status: {response.status_code}, Text: {response.text}")
                return redirect(url_for('login_page', msg="Lỗi hệ thống: Không parse được response từ SSO"))


            # 3. Truy cập các trường lỗi bằng dictionary data
            error = data.get("error", "unknown_error")
            error_description = data.get("error_description", f"Lỗi không xác định ({response.status_code})")
                        
            print(f"Lỗi khi exchange token ({error}): {error_description}")
            return redirect(url_for('login_page', msg=f"Lỗi SSO: {error_description}"))

        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        id_token = tokens.get("id_token")
        expires_in = tokens.get("expires_in", 3600)
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        
        # Gọi userinfo endpoint
        userinfo_response = requests.get(
            "http://localhost:5001/api/auth/user-info",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )

        if userinfo_response.status_code != 202:
            return f"Lỗi khi lấy thông tin user: {userinfo_response.text}"

        user_info = userinfo_response.json()
        username = user_info.get("username")
        fullname = user_info.get("fullname")
        avatar = user_info.get("avatar")
        
        # Mở kết nối và bắt đầu transaction
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        user_id = None # Khởi tạo user_id
        
        try:
            # 1. Tìm user
            cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
            user_row = cursor.fetchone()
            
            if not user_row:
                new_user_id = str(uuid.uuid4())

                # 2. Tạo user mới nếu không tồn tại
                cursor.execute("""
                    INSERT INTO users (id, username, fullname, avatar)
                    VALUES (%s, %s, %s, %s)
                """, (new_user_id, username, fullname, avatar))
                # Lấy ID của bản ghi vừa được tạo
                user_id = new_user_id
            else:
                user_id = user_row['id']
            
            # KIỂM TRA TÍNH HỢP LỆ CỦA user_id
            if not user_id:
                # Nếu không thể lấy được ID sau khi INSERT, rollback và báo lỗi
                conn.rollback()
                print("LỖI: Không lấy được user_id sau khi tạo user mới.")
                return redirect(url_for('login_page', msg="Lỗi hệ thống: Không xác định được User ID"))
            
            # 3. Tạo token riêng MyBK
            mybk_token = secrets.token_urlsafe(32)
            
            # 4. Lưu token vào DB
            cursor.execute("""
                INSERT INTO tokens (user_id, token, access_token, refresh_token, expires_at)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    token=VALUES(token),
                    access_token=VALUES(access_token),
                    refresh_token=VALUES(refresh_token),
                    expires_at=VALUES(expires_at)
            """, (user_id, mybk_token, access_token, refresh_token, expires_at))
            
            # Commit toàn bộ transaction nếu không có lỗi
            conn.commit()
        except Exception as e:
            # Nếu có bất kỳ lỗi nào, rollback
            conn.rollback()
            print(f"LỖI DATABASE (IntegrityError/Khác): {e}")
            return redirect(url_for('login_page', msg="Lỗi hệ thống: Lỗi lưu trữ dữ liệu"))

        finally:
            pass
        
        # Lưu session frontend
        session['username'] = username
        session['is_logged_in'] = True
        session['mybk_token'] = mybk_token
        
        return redirect(url_for('mybk_dashboard'))
    
    return "Lỗi: Không nhận được mã xác thực từ SSO Server."


@app.route('/register')
def register_page():
    return redirect(f"{SSO_SERVER_URL}/register")

@app.route('/logout')
def logout():

    session.clear() 
    SSO_LOGOUT_URL = "http://localhost:5000/logout" 
    global_logout_url = f"{SSO_LOGOUT_URL}?redirect={SERVICE_URL}"

    return redirect(global_logout_url)


if __name__ == '__main__':
    print(f" Starting MyBK Service on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)