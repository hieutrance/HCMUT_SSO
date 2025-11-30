import { useState, useEffect } from "react";
import logo from "../assets/images/logo.png";
import axios from "axios";
import { useParams } from "react-router-dom";

const apiUrl = "http://localhost:5001/api";

const setSessionCookie = (name, value, expirySeconds) => {
    // ExpirySeconds là thời gian tồn tại tối đa tính bằng giây
    // Chúng ta sử dụng UTC để đảm bảo tính nhất quán trên các múi giờ
    const expires = new Date();
    expires.setTime(expires.getTime() + expirySeconds * 1000); 
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; secure; samesite=Lax`;
    
    // Lưu session exp dưới dạng timestamp để kiểm tra trong useEffect
    const expiryTimestamp = Math.floor(Date.now() / 1000) + expirySeconds;
    document.cookie = `browser_session_exp=${expiryTimestamp}; expires=${expires.toUTCString()}; path=/; secure; samesite=Lax`;
  };

export default function Login() {
  const params = new URLSearchParams(window.location.search);
  const response_type = params.get("response_type");
  const scope = params.get("scope");
  const client_id = params.get("client_id");
  const redirect_uri = params.get("redirect_uri");

  function getCookie(name) {
    const value = document.cookie
      .split("; ")
      .find((row) => row.startsWith(name + "="));
    return value ? value.split("=")[1] : null;
  }

  useEffect(() => {
    async function checkSessionAndAuthenticate() {
      const browser_session = getCookie("browser_session");
      const browser_session_exp = getCookie("browser_session_exp");
      
      console.log("Browser session =", browser_session);
      console.log("Browser session exp =", browser_session_exp);

      // Nếu không có session hoặc các tham số OAuth/OIDC cơ bản, dừng lại.
      if (!browser_session || !browser_session_exp || !response_type || !client_id || !redirect_uri) return;

      const now = new Date(); 
      const expiryTime = new Date(browser_session_exp);
      
      // Kiểm tra session hết hạn (sử dụng đối tượng Date)
      if (now >= expiryTime) {
        console.log("Session expired. Clearing cookies.");
        // Xóa cookie hết hạn
        document.cookie = "browser_session=; Max-Age=0; path=/; secure; samesite=Lax";
        document.cookie = "browser_session_exp=; Max-Age=0; path=/; secure; samesite=Lax";
        return;
      }
      
      // Hiển thị thông báo đang tự động đăng nhập (nếu cần)
      // setGeneralError("Đang tự động xác thực lại session...");
      
      // TỰ ĐỘNG GỌI API ĐỂ XÁC THỰC LẠI BẰNG SESSION ĐÃ LƯU
      try {
        console.log("Attempting auto-authentication with existing session...");
        const response = await axios.post(`${apiUrl}/auth/authenticate`, {
          response_type: response_type,
          scope: scope,
          client_id: client_id,
          redirect_uri: redirect_uri,
          session: browser_session // Gửi session token đã lưu
        });

        console.log("Response from auto-authentication:", response.data);
        
        const {
            authentication_code: authorization_code,
            redirect_uri: n_redirect_uri,
            browser_session: new_browser_session, // Session mới nếu được refresh
            browser_session_exp_seconds // Thời hạn mới tính bằng giây
        } = response.data;
        
        // Cập nhật lại session nếu server trả về session mới (refresh token)
        if (new_browser_session) {
          const expiry = browser_session_exp_seconds || DEFAULT_SESSION_EXPIRY_SECONDS;
          setSessionCookie("browser_session", new_browser_session, expiry);
          console.log("Browser session refreshed and set successfully.");
        } 

        // Chuyển hướng nếu nhận được mã ủy quyền
        if (authorization_code && n_redirect_uri) {
          window.location.href = `${n_redirect_uri}?code=${authorization_code}`;
          return; // Ngăn chặn render form login
        } else {
          console.error("Missing authorization_code or redirect_uri in auto-auth response. User must log in.");
          // Để người dùng đăng nhập thủ công
        }

      } catch (error) {
        // Nếu API tự động xác thực thất bại, xóa session cũ và để người dùng đăng nhập thủ công.
        console.warn("Auto-authentication failed. Clearing session and prompting manual login.");
        setGeneralError("Session đã hết hạn hoặc không hợp lệ. Vui lòng đăng nhập lại.");
        document.cookie = "browser_session=; Max-Age=0; path=/; secure; samesite=Lax";
        document.cookie = "browser_session_exp=; Max-Age=0; path=/; secure; samesite=Lax";
      }
    }
    
    checkSessionAndAuthenticate();

  }, [response_type, scope, client_id, redirect_uri]);

  const [usernameError, setUsernameError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    console.log(`API ${apiUrl}/auth/authenticate`);
    console.log({ username, password });

    try {
      const response = await axios.post(`${apiUrl}/auth/authenticate`, {
        response_type: response_type,
        scope: scope,
        client_id: client_id,
        redirect_uri: redirect_uri,
        username: username,
        password: password,
      });

      console.log("Response from backend:", response.data);
      let authorization_code = response.data.authentication_code;
      let n_redirect_uri = response.data.redirect_uri;

      let browser_session = response.data.browser_session;
      let browser_session_exp = response.data.browser_session_exp;
      
      if (browser_session) {
        const expiry = 3600*24*7;
        setSessionCookie("browser_session", browser_session, expiry);
        setSessionCookie("browser_session_exp", browser_session_exp, expiry);
        console.log("Browser session set successfully.");
      } else {
        console.warn("Backend response does not contain 'browser_session'. Session cookie was not set.");
      }

      if (authorization_code && n_redirect_uri) {
        window.location.href = `${n_redirect_uri}?code=${authorization_code}`;
      } else {
        console.error("Missing authorization_code or redirect_uri in response");
      }
    } catch (error) {
      if (error.response) {
        const errCode = error.response.data.error;
        const errDesc = error.response.data.error_description;
        if (errCode == "wrong_username") {
          setUsernameError(true);
          setPasswordError(false); // Đảm bảo chỉ 1 lỗi được hiển thị
        } else if (errCode == "wrong_password") {
          // Dùng else if
          setPasswordError(true);
          setUsernameError(false); // Đảm bảo chỉ 1 lỗi được hiển thị
        } else {
          // Xử lý các lỗi khác từ backend (ví dụ: client_id không hợp lệ,...)
          console.error("Backend error:", errCode, errDesc);
          alert(`Lỗi: ${errDesc || "Đăng nhập không thành công."}`);
        }
      } else if (error.request) {
        console.error(
          "Không có phản hồi từ máy chủ. Kiểm tra kết nối mạng/API server:",
          error.request
        );
        alert("Không kết nối được với máy chủ API.");
      } else {
        console.error("Lỗi khi thiết lập yêu cầu:", error.message);
        alert("Đã xảy ra lỗi không xác định.");
      }
    }
  }

  return (
    <div className="bg-white p-20 w-5/12">
      {/* Logo Header */}
      <div className="flex items-center text-blue-900 mb-6">
        <img src={logo} alt="HCMUT Logo" className="w-10 h-10 mr-3" />
        <div className="flex flex-col">
          <strong className="text-2xl font-bold">HCMUT SSO</strong>
          <span className="text-sm font-semibold text-blue-700">by OIDC</span>
        </div>
      </div>

      {/* Form Title */}
      <h2 className="text-3xl font-bold text-blue-900 mb-6">Đăng nhập</h2>

      {/* SỬA LỖI: Bọc tất cả vào thẻ <form> và thêm onSubmit */}
      <form className="space-y-5" onSubmit={handleSubmit}>
        <input type="hidden" name="response_type" value={response_type || ""} />
        <input type="hidden" name="scope" value={scope || ""} />
        <input type="hidden" name="client_id" value={client_id || ""} />
        <input type="hidden" name="redirect_uri" value={redirect_uri || ""} />

        {/* Username */}
        <div className="flex flex-col">
          <label
            htmlFor="username"
            className="font-semibold text-gray-700 mb-1"
          >
            Tên tài khoản
          </label>
          <input
            type="text"
            id="username"
            name="username"
            required
            value={username}
            onChange={(e) => {
              setUsername(e.target.value);
              setUsernameError(false);
            }}
            className={`px-4 py-3 rounded-lg bg-blue-50 text-blue-900 focus:outline-none focus:ring-2 
              ${
                usernameError
                  ? "border border-red-500 focus:ring-red-400"
                  : "focus:ring-blue-500"
              }`}
          />

          {usernameError && (
            <span className="text-red-600 text-sm mt-1">
              Tên đăng nhập không đúng.
            </span>
          )}
        </div>

        {/* Password */}
        <div className="flex flex-col">
          <label
            htmlFor="password"
            className="font-semibold text-gray-700 mb-1"
          >
            Mật khẩu
          </label>
          <input
            type="password"
            id="password"
            name="password"
            required
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setPasswordError(false);
            }}
            className={`px-4 py-3 rounded-lg bg-blue-50 text-blue-900 focus:outline-none focus:ring-2 
              ${
                passwordError
                  ? "border border-red-500 focus:ring-red-400"
                  : "focus:ring-blue-500"
              }`}
          />

          {passwordError && (
            <span className="text-red-600 text-sm mt-1">
              Mật khẩu không đúng.
            </span>
          )}
        </div>

        {/* Submit - SỬA LỖI: Chuyển div thành button type="submit" */}
        <button
          type="submit"
          className="w-full py-3 rounded-lg bg-blue-900 text-white font-semibold text-lg hover:bg-blue-800 transition"
        >
          Đăng nhập
        </button>
      </form>

      {/* Footer links */}
      <div className="mt-6 flex flex-col gap-3 text-center">
        <a
          href="/forgetpassword"
          className="text-blue-700 font-semibold hover:underline"
        >
          Quên mật khẩu?
        </a>
        <a
          href="/register"
          className="text-blue-700 font-semibold hover:underline"
        >
          Chưa có tài khoản? Đăng ký
        </a>
      </div>
    </div>
  );
}
