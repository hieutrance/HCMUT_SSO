import os
from flask import Flask, render_template, redirect, request, url_for

# Đặt port 
SSO_PORT = 5001

app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route('/login', methods=['GET', 'POST'])
def login_page_sso():

    # Lấy tham số redirect_uri từ URL từ Client gửi 
    redirect_to_client = request.args.get('redirect_uri')
    
    if request.method == 'POST':
        if redirect_to_client:
            print(f"Đăng nhập thành công. Chuyển hướng về: {redirect_to_client}")
            return redirect(redirect_to_client)
        else:
            return "Lỗi: Không tìm thấy địa chỉ chuyển hướng (redirect_uri) về Client."


    return render_template('sso_server/loginpage.html')


# XỬ LÝ ĐĂNG KÝ
@app.route('/register')
def register_page():
    return render_template('sso_server/register.html')

# xỬ LÝ QUÊN MẬT KHẨU
@app.route('/forgetpassword')
def forget_password_page():

    return render_template('sso_server/forgetpassword.html')

# --- KHỞI CHẠY ---
if __name__ == '__main__':
    print(f"Starting SSO Server on port {SSO_PORT}")
    app.run(host='0.0.0.0', port=SSO_PORT, debug=True)