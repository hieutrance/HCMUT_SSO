import os
from flask import Flask, render_template, redirect, url_for, session, request

# --- CẤU HÌNH CHO LMS ---
SERVICE_PORT = 4000  # Chạy trên cổng 5002
SERVICE_URL = f"http://localhost:{SERVICE_PORT}"

# Cấu hình kết nối tới SSO Server
SSO_SERVER_URL = "http://localhost:5000" 
CLIENT_ID = "lms_service_client"

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


@app.route('/lms')
@app.route('/dashboard')
def lms_dashboard():
    if not session.get('is_logged_in'):
        # Chưa đăng nhập -> Chuyển hướng sang route login để bắt đầu SSO
        return redirect(url_for('login_page'))
    
    return render_template('Lms.html', username=session.get('username'))


@app.route('/login')
def login_page():
    # URL mà SSO Server sẽ gọi lại sau khi đăng nhập thành công
    callback_url = f"{SERVICE_URL}/sso_callback"
    
    sso_redirect_url = (
        f"{SSO_SERVER_URL}/authorize?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={callback_url}"
    )
    
    return redirect(sso_redirect_url)



@app.route('/sso_callback')
def sso_callback():
    # Lấy authorization code từ URL (nếu có)
    auth_code = request.args.get('code')
    
    if auth_code:
        session['username'] = 'sinhvien' 
        session['is_logged_in'] = True
        
        # Đăng nhập xong -> Vào thẳng lms
        return redirect(url_for('lms_dashboard'))
    
    return "Lỗi: Không nhận được mã xác thực từ SSO Server."


@app.route('/register')
def register_page():
    return redirect(f"{SSO_SERVER_URL}/register")


@app.route('/logout')
def logout():
    session.clear()

    return redirect(f"{SSO_SERVER_URL}/logout")



if __name__ == '__main__':
    print(f"Starting LMS Service on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)