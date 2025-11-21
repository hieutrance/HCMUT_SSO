import React from "react";
import LoginForm from "./components/LoginForm";
import bg1 from "./assets/bg1.jpg";
import bg2 from "./assets/bg2.jpg";
export default function App() {
  return (
    // <div
    //   className="relative flex items-center justify-center min-h-screen font-sans overflow-hidden"
    // >
    //   {/* Nền 1 */}
    //   <div
    //     className="absolute inset-0 -z-20 bg-cover bg-center"
    //     style={{ backgroundImage: `url(${bg1})` }}
    //   ></div>

    //   {/* Nền 2 có hiệu ứng mờ chồng */}
    //   <div
    //     className="absolute inset-0 -z-10 bg-cover bg-center opacity-0 animate-fadeSlide"
    //     style={{ backgroundImage: `url(${bg2})` }}
    //   ></div>

    //   {/* Form */}
    //   <LoginForm />
    // </div>
    <body>

    <div class="form-container">
        <div class="form-header-register">
            <div class="logo-header">
                <img src="./asset/logo.png" alt="HCMUT Logo" class="logo"/>
                <div class="logo-text">
                    <strong>HCMUT SSO</strong>
                    <span>by OIDC</span>
                </div>
            </div>
            <h2 class="form-title-register">Đăng Ký</h2>
        </div>

        <form action="#" method="POST">
            <div class="form-group">
                <label for="username">Tên tài khoản</label>
                <input type="text" id="username" name="username" required />
            </div>

            <div class="form-group">
                <label for="email">E-mail</label>
                <input type="email" id="email" name="email" required />
            </div>

            <div class="form-group">
                <label for="password">Mật khẩu</label>
                <input type="password" id="password" name="password" required />
            </div>

            <div class="form-group">
                <label for="confirm-password">Xác nhận mật khẩu</label>
                <input type="password" id="confirm-password" name="confirm-password" required />
            </div>

            <button type="submit" class="btn-submit">Đăng Ký</button>
        </form>

        <div class="form-footer">
            <a href="loginpage.html">Đã có tài khoản? Đăng nhập</a>
        </div>
    </div>

    <script src="script.js"></script>

</body>
  );
}
