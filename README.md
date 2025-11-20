OIDC Demo Authentication – Flask Client & SSO Server

Dự án mô phỏng cơ chế Single Sign-On (SSO) theo mô hình OIDC (OpenID Connect), gồm 2 ứng dụng Flask chạy độc lập:

Client App – Ứng dụng cần xác thực (Relying Party)

SSO Server – Máy chủ cung cấp đăng nhập, token, xác thực người dùng (Identity Provider)

Mục tiêu của dự án là xây dựng quy trình login SSO cơ bản, gồm:

Redirect sang trang đăng nhập chung

Xác thực người dùng tại SSO Server

Trả về mã phiên (session/token)

Client nhận token → cho phép truy cập vào trang bảo vệ

🔧 Công nghệ sử dụng

Python 3.x

Flask

HTML/CSS/JS

OIDC flow cơ bản (mô phỏng logic redirect + login session)

📁 Cấu trúc thư mục
BTL_MMANM/
│
├── Client/
│   ├── static/
│   │   ├── css/style_client.css
│   │   ├── js/script_client.js
│   │   └── images/
│   ├── templates/client/
│   │   ├── Homepage.html
│   │   ├── Lms.html
│   │   └── Mybk.html
│   └── app.py
│
└── SSO_Server/
    ├── static/
    │   ├── css/style_server.css
    │   ├── js/script_server.js
    │   └── images/
    ├── templates/sso_server/
    │   ├── loginpage.html
    │   ├── register.html
    │   └── forgetpassword.html
    └── app.py

🚀 Cách chạy dự án
1. Clone repo
git clone <link_repo_cua_ban>
cd BTL_MMANM

2. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

3. Cài dependencies

(Trong dự án nếu bạn có file requirements.txt thì sửa lại lệnh dưới)

pip install flask

4. Chạy Client
cd Client
python app.py


Client sẽ chạy tại:
➡ http://127.0.0.1:5000

5. Chạy SSO Server

Mở terminal thứ hai:

cd SSO_Server
python app.py


SSO Server sẽ chạy tại:
➡ http://127.0.0.1:5001

🔑 Luồng OIDC mô phỏng

Người dùng truy cập Client (http://127.0.0.1:5000
).

Client kiểm tra trạng thái đăng nhập → chưa đăng nhập → redirect sang:

http://127.0.0.1:5001/login


Người dùng nhập tài khoản/mật khẩu tại SSO Server.

SSO Server xác thực → tạo session → gửi token/flag authenticated về Client.

Client nhận token → cho phép truy cập trang đã bảo vệ (Homepage/Lms/Mybk).
