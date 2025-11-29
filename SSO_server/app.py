import os
from flask import Flask, render_template, request, redirect, url_for, session
from routes.auth import auth_bp
from routes.client import client_bp
from routes.test import test_bp
from db import execute_sql
from utils.security import hash_password, verify_password
import secrets
import datetime

app = Flask(__name__)
# Key bí mật cho session của SSO Server
app.secret_key = "sso_super_secret_key_global" 
# Đặt tên cookie riêng để tránh xung đột
app.config['SESSION_COOKIE_NAME'] = 'sso_session'

def redirect_with_code(redirect_uri):
    auth_code = secrets.token_urlsafe(32)
    
    # Ghép mã code vào URL redirect
    if "?" in redirect_uri:
        final_redirect = f"{redirect_uri}&code={auth_code}"
    else:
        final_redirect = f"{redirect_uri}?code={auth_code}"
        
    print(f"🔄 Đã đăng nhập. Chuyển hướng về: {final_redirect}")
    return redirect(final_redirect)

@app.route('/authorize')
def render_authoration_ui():
    # Nhận các tham số OIDC
    scope = request.args.get("scope")
    response_type = request.args.get("response_type")
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")

    # Nếu đã đăng nhập, chuyển hướng luôn không cần hiện form
    if 'sso_user_id' in session and redirect_uri:
        return redirect_with_code(redirect_uri)

    # Nếu chưa đăng nhập, chuyển sang trang login 
    return render_template('loginpage.html',
                           scope=scope,
                           response_type=response_type,
                           client_id=client_id,
                           redirect_uri=redirect_uri)

# --- ROUTE LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login_page_sso():
    redirect_to_client = request.args.get('redirect_uri') or request.form.get('redirect_uri')
    
    # kiểm tra session cũ
    if 'sso_user_id' in session:
        print(f"✅ Phát hiện phiên đăng nhập cũ: {session.get('sso_username')}")
        if redirect_to_client and redirect_to_client != 'None':
            return redirect_with_code(redirect_to_client)
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Query database tìm user
        user = execute_sql("SELECT * FROM users WHERE username=%s", (username,), True)
        
        if user and verify_password(password, user['password']):
            print("✅ Đăng nhập mới thành công!")
            
            # Lưu session
            session['sso_user_id'] = user['id']
            session['sso_username'] = user['username']
            session.permanent = True 
            
            if redirect_to_client and redirect_to_client != 'None':
                return redirect_with_code(redirect_to_client)
            else:
                return "Đăng nhập thành công (Không có Client để quay về)."
        else:
            return render_template('loginpage.html', redirect_uri=redirect_to_client, error="Sai thông tin đăng nhập")

    return render_template('loginpage.html', redirect_uri=redirect_to_client)

# --- ROUTE ĐĂNG KÝ ---
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # Lấy redirect_uri từ URL hoặc Form
    redirect_uri = request.args.get('redirect_uri') or request.form.get('redirect_uri')
    print(f"DEBUG REGISTER: redirect_uri nhận được là: {redirect_uri}")
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm_password = request.form.get('confirm-password')
        
        # 1. Kiểm tra mật khẩu xác nhận
        if password != confirm_password:
            return render_template('register.html', redirect_uri=redirect_uri, error="Mật khẩu không khớp")

        # 2. Kiểm tra user đã tồn tại chưa
        existing_user = execute_sql("SELECT * FROM users WHERE username=%s", (username,), True)
        if existing_user:
            return render_template('register.html', redirect_uri=redirect_uri, error="Tài khoản đã tồn tại")

        # 3. Hash mật khẩu và Lưu vào DB
        hashed_pw = hash_password(password)
        
        insert_result = execute_sql(
            "INSERT INTO users (username, password, email, fullname) VALUES (%s, %s, %s, %s)",
            (username, hashed_pw, email, username)
        )
        
        # 4. Xử lý kết quả đăng ký
        if insert_result:
            print(f"✅ Đăng ký thành công user: {username}")
            
            # Điều hướng về trang đăng nhập (kèm redirect_uri nếu có)
            if redirect_uri and redirect_uri != 'None':
                return redirect(url_for('login_page_sso', redirect_uri=redirect_uri))
            else:
                return redirect(url_for('login_page_sso'))
        else:
            # Trường hợp lỗi DB
            return render_template('register.html', redirect_uri=redirect_uri, error="Lỗi hệ thống, không thể tạo tài khoản")

    # GET Request: Hiển thị form đăng ký
    return render_template('register.html', redirect_uri=redirect_uri)


@app.route('/forgetpassword')
def forget_password_page():
    return render_template('forgetpassword.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login_page_sso'))

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(client_bp, url_prefix="/api/client")
app.register_blueprint(test_bp, url_prefix="/api/test" )

if __name__ == "__main__":
    print("🚀 Starting SSO Server on http://localhost:5000")
    app.run(debug=True, port=5000)