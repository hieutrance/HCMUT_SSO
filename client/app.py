import os
from flask import Flask, render_template, redirect, url_for, session, request

# CẤU HÌNH PORT 
CLIENT_PORT = 5000
# ĐƯỜNG DẪN ĐẾN SSO SERVER
SSO_SERVER_URL = "http://localhost:5001" 

app = Flask(__name__)
app.secret_key = os.urandom(24)


###############################################################

@app.route('/')
@app.route('/home')
def home_page():
    user_info = {
        'username': session.get('username', 'Khách'),
        'is_logged_in': session.get('is_logged_in', False)
    }
    return render_template('client/Homepage.html', **user_info)

###############################################################
@app.route('/lms')
def lms_service():
    if not session.get('is_logged_in'):
        return redirect(url_for('login_page')) # Nếu chưa login direct đến trang login của SSO
    
    return render_template('client/Lms.html', username=session.get('username'))

###############################################################
@app.route('/mybk')
def mybk_service():
    if not session.get('is_logged_in'):
        return redirect(url_for('login_page'))
        
    return render_template('client/Mybk.html', username=session.get('username'))


###############################################################
@app.route('/login')
def login_page():
    callback_url = f"http://localhost:{CLIENT_PORT}/sso_callback"
    
    # Chuyển hướng sang trang login của SSO Server 
    sso_login_url = f"{SSO_SERVER_URL}/login?redirect_uri={callback_url}"
    
    return redirect(sso_login_url)


###############################################################
@app.route('/sso_callback')
def sso_callback():
    session['username'] = 'SinhVien'
    session['is_logged_in'] = True
    
    return redirect(url_for('home_page'))

###############################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_page'))

@app.route('/register')
def register_page():
    return redirect(f"{SSO_SERVER_URL}/register")

###############################################################
if __name__ == '__main__':
    print(f"Starting Client SP on port {CLIENT_PORT}")
    app.run(host='0.0.0.0', port=CLIENT_PORT, debug=True)