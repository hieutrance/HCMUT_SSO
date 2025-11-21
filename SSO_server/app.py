import os
from flask import Flask, render_template, redirect, request, url_for, session

# --- CẤU HÌNH ---
SSO_PORT = 5000

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- CÁC ROUTE SSO SERVER ---

@app.route('/login', methods=['GET', 'POST'])
def login_page_sso():
    # Lấy tham số redirect_uri (Ưu tiên từ URL, sau đó đến Form)
    redirect_to_client = request.args.get('redirect_uri') or request.form.get('redirect_uri')
    
    if request.method == 'POST':
        # Lấy thông tin từ form
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"User {username} đang đăng nhập...")

        if redirect_to_client:
            # Giả lập code xác thực
            auth_code = "gialap_code_123456"
            
            # Ghép code vào URL redirect
            if "?" in redirect_to_client:
                final_redirect = f"{redirect_to_client}&code={auth_code}"
            else:
                final_redirect = f"{redirect_to_client}?code={auth_code}"
                
            print(f"Đăng nhập thành công. Chuyển hướng về: {final_redirect}")
            return redirect(final_redirect)
        else:
            return "Đăng nhập thành công trên SSO Server (Không có Client để quay về)."

    # SỬA LỖI: Bỏ 'sso_server/' vì file nằm ngay trong templates/
    return render_template('loginpage.html', redirect_uri=redirect_to_client)

@app.route('/register')
def register_page():
    # SỬA LỖI: Bỏ 'sso_server/'
    return render_template('register.html')

@app.route('/forgetpassword')
def forget_password_page():
    # SỬA LỖI: Bỏ 'sso_server/'
    return render_template('forgetpassword.html')

# --- KHỞI CHẠY ---
if __name__ == '__main__':
    print(f"Starting SSO Server on port {SSO_PORT}")
    app.run(host='0.0.0.0', port=SSO_PORT, debug=True)