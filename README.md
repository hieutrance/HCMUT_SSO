# HCMUT SSO by OIDC
A simulation of a Single Sign-On (SSO) system using the OpenID Connect (OIDC) protocol, built with Python Flask. This project demonstrates the interaction between a Service Provider (SP) and an Identity Provider (IdP) in a distributed environment.

🌟 Features

Distributed Architecture: Separate Client (SP) and SSO Server (IdP) applications running on different ports.

SSO Login Flow: Redirects unauthenticated users from the Client to the SSO Server for centralized login.

Mock Authentication: Simulates the login process without a real database (for educational purposes).

Cross-Domain Redirects: Demonstrates the redirect flow between localhost:5000 and localhost:5001.

Responsive UI: Clean and modern user interface for Homepage, Login, and Register pages.

Dynamic Backgrounds: Login pages feature a slideshow background script.

Dự án gồm 2 phần ứng dụng chạy song song:
- **Client App** – cổng dịch vụ chính  
- **SSO Server** – hệ thống xác thực Single Sign-On  

## 🚀 1. Cấu trúc thư mục

<pre>
BTL_MMANM/
├── .venv/                      # Shared Virtual Environment
├── Client/                     # Service Provider (Runs on Port 5000)
│   ├── app.py                  # Client logic (LMS, MyBK services)
│   ├── static/                 # Client assets (CSS, JS, Images)
│   └── templates/
│       └── client/             # Client HTML pages
├── SSO_Server/                 # Identity Provider (Runs on Port 5001)
│   ├── app.py                  # SSO logic (Login, Auth)
│   ├── static/                 # Server assets
│   └── templates/
│       └── sso_server/         # Server HTML pages
└── README.md
</pre>



## ⚙️ 2. Cách chạy dự án

### 📌 **Yêu cầu**
- Python 3.x  
- Flask  
- Các thư viện có trong `requirements.txt` (nếu có)

### ▶️ **Khởi tạo môi trường ảo**
```
.\.venv\Scripts\activate
```
### ▶️ **Chạy SSO Server**

```bash
cd SSO_Server
python app.py
```

Ứng dụng chạy tại:
```
http://127.0.0.1:5001
cd SSO_Server
python app.py
```
### ▶️ **Chạy Client**
```
cd Client
python app.py
```
Ứng dụng chạy tại:
```
http://127.0.0.1:5000
cd Client
python app.py
```
🔗 3. Luồng hoạt động hệ thống

Người dùng truy cập Client tại 127.0.0.1:5000

Khi cần login, Client chuyển hướng sang SSO Server (127.0.0.1:5001)

Sau khi đăng nhập thành công, SSO trả token và chuyển người dùng về lại Client

Client xác thực token và cho phép truy cập các trang như:

- Homepage

- LMS

- MyBK


🧪 4. Tính năng chính
✔️ Client

- Tích hợp đăng nhập qua SSO

- Hiển thị các trang dịch vụ (Homepage, LMS, MyBK)

- Xử lý token từ SSO

✔️ SSO Server

- Đăng nhập

- Đăng ký

- Quên mật khẩu

- Trả token xác thực về Client


📌 5. Ghi chú

Hai server phải chạy độc lập trên 2 port khác nhau:

- Client → 5000

- SSO → 5001

Token truyền giữa Client ↔ SSO có thể là JWT hoặc session key tùy bạn triển khai.
