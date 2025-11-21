import os
from flask import Flask, render_template, redirect, url_for, session, request


SERVICE_PORT = 3000 
SERVICE_URL = f"http://localhost:{SERVICE_PORT}"

SSO_SERVER_URL = "http://localhost:5001" 
CLIENT_ID = "mybk_service_client"

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


@app.route('/mybk')
@app.route('/dashboard')
def mybk_dashboard():

    if not session.get('is_logged_in'):
        # Chưa đăng nhập -> Chuyển hướng sang route login để bắt đầu SSO
        return redirect(url_for('login_page'))
    
    return render_template('Mybk.html', username=session.get('username'))


@app.route('/login')
def login_page():
    # URL mà SSO Server sẽ gọi lại sau khi đăng nhập thành công
    callback_url = f"{SERVICE_URL}/sso_callback"
    
    # Tạo URL chuyển hướng kèm tham số
    sso_redirect_url = (
        f"{SSO_SERVER_URL}/login?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={callback_url}"
    )
    
    return redirect(sso_redirect_url)

@app.route('/sso_callback')
def sso_callback():
    # Lấy authorization code từ URL
    auth_code = request.args.get('code')
    
    if auth_code:
        # Giả lập xác thực thành công và lưu thông tin vào Session của MyBK
        session['username'] = 'sinvien' 
        session['is_logged_in'] = True
        
        # Đăng nhập xong -> Vào thẳng trang Mybk
        return redirect(url_for('mybk_dashboard'))
    
    return "Lỗi: Không nhận được mã xác thực từ SSO Server."



@app.route('/register')
def register_page():
    return redirect(f"{SSO_SERVER_URL}/register")

@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    print(f" Starting MyBK Service on port {SERVICE_PORT}")
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)