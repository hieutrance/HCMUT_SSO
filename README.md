# BTL_MMANM – Client & SSO Authentication System

Dự án gồm 2 phần ứng dụng chạy song song:
- **Client App** – cổng dịch vụ chính  
- **SSO Server** – hệ thống xác thực Single Sign-On  

## 🚀 1. Cấu trúc thư mục

<ul>
<li><strong>BTL_MMANM/</strong>
<ul>
<li><code>.venv/</code> &nbsp; <em># Shared Virtual Environment</em></li>
<li><strong>Client/</strong> &nbsp; <em># Service Provider (Runs on Port 5000)</em>
<ul>
<li><code>app.py</code> &nbsp; <em># Client logic (LMS, MyBK services)</em></li>
<li><strong>static/</strong> &nbsp; <em># Client assets (CSS, JS, Images)</em></li>
<li><strong>templates/</strong>
<ul>
<li><strong>client/</strong> &nbsp; <em># Client HTML pages</em></li>
</ul>
</li>
</ul>
</li>
<li><strong>SSO_Server/</strong> &nbsp; <em># Identity Provider (Runs on Port 5001)</em>
<ul>
<li><code>app.py</code> &nbsp; <em># SSO logic (Login, Auth)</em></li>
<li><strong>static/</strong> &nbsp; <em># Server assets</em></li>
<li><strong>templates/</strong>
<ul>
<li><strong>sso_server/</strong> &nbsp; <em># Server HTML pages</em></li>
</ul>
</li>
</ul>
</li>
<li><code>README.md</code></li>
</ul>
</li>
</ul>

## ⚙️ 2. Cách chạy dự án

### 📌 **Yêu cầu**
- Python 3.x  
- Flask  
- Các thư viện có trong `requirements.txt` (nếu có)
  
```bash
### ▶️ **Chạy SSO Server**

cd SSO_Server
python app.py

Ứng dụng chạy tại:
http://127.0.0.1:5001
cd Client
python app.py

### ▶️ **Chạy Client**
cd Client
python app.py

Ứng dụng chạy tại:
http://127.0.0.1:5000

🔗 3. Luồng hoạt động hệ thống

Người dùng truy cập Client tại 127.0.0.1:5000

Khi cần login, Client chuyển hướng sang SSO Server (127.0.0.1:5001)

Sau khi đăng nhập thành công, SSO trả token và chuyển người dùng về lại Client

Client xác thực token và cho phép truy cập các trang như:

Homepage

LMS

MyBK


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

Client → 5000

SSO → 5001

Token truyền giữa Client ↔ SSO có thể là JWT hoặc session key tùy bạn triển khai.
