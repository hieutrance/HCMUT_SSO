import os
from flask import Flask, render_template, redirect, url_for, session, request

# --- CẤU HÌNH ---
SERVICE_PORT = 3000 
SERVICE_URL = f"http://localhost:{SERVICE_PORT}"

# Giả sử SSO chạy port 5000 (như bạn cấu hình)
SSO_SERVER_URL = "http://localhost:5000" 
CLIENT_ID = "mybk_service_client"

app = Flask(__name__)

# 1. Dùng Secret Key cố định (Tránh mất session khi server restart)
app.secret_key = "mybk_super_secret_key" 

# 2. QUAN TRỌNG: Đặt tên Cookie riêng biệt để không bị trùng với LMS/SSO
app.config['SESSION_COOKIE_NAME'] = 'mybk_session'

@app.route('/')
@app.route('/home')
def home_page():
    user_info = {
        'username': session.get('username', 'Khách'),
        'is_logged_in': session.get('is_logged_in', False)
    }
    return render_template('Homepage.html', **user_info)

@app.route('/mybk')
@app.route('/dashboard')
def mybk_dashboard():
    # Kiểm tra session
    if not session.get('is_logged_in'):
        return redirect(url_for('login_page'))
    
    return render_template('Mybk.html', username=session.get('username'))

@app.route('/login')
def login_page():
    callback_url = f"{SERVICE_URL}/sso_callback"
    
    sso_redirect_url = (
        f"{SSO_SERVER_URL}/login?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={callback_url}"
    )
    return redirect(sso_redirect_url)

@app.route('/sso_callback')
def sso_callback():
    auth_code = request.args.get('code')
    
    if auth_code:
        # Tạo session MyBK thành công
        session['username'] = 'SinhVien_MyBK' 
        session['is_logged_in'] = True
        
        # Chuyển hướng thẳng vào Dashboard
        return redirect(url_for('mybk_dashboard'))
    
    return "Lỗi: Không nhận được mã xác thực."

@app.route('/register')
def register_page():
    return redirect(f"{SSO_SERVER_URL}/register")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f"{SSO_SERVER_URL}/logout")

if __name__ == '__main__':
    print(f"🚀 Starting MyBK Service on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)