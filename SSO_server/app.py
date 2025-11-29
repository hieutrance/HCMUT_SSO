from flask import Flask, render_template, request
from routes.auth import auth_bp
from routes.client import client_bp
from routes.test import test_bp

app = Flask(__name__)


@app.route('/authorize')
def render_authoration_ui():

    scope = request.args.get("scope")
    response_type = request.args.get("response_type")
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")

    print(scope, response_type, client_id, redirect_uri)

    return render_template('loginpage.html',
                           scope=scope,
                           response_type=response_type,
                           client_id=client_id,
                           redirect_uri=redirect_uri)
    

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

    return render_template('loginpage.html', redirect_uri=redirect_to_client)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template('register.html')

@app.route('/forgetpassword')
def forget_password_page():
    return render_template('forgetpassword.html')



app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(client_bp, url_prefix="/api/client")
app.register_blueprint(test_bp, url_prefix="/api/test" )



if __name__ == "__main__":
    app.run(debug=True)
