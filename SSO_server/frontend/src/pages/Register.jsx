import { useState, useEffect } from "react";
import logo from "../assets/images/logo.png";
import axios from "axios";

const apiUrl = "http://localhost:5001/api";

const setSessionCookie = (name, value, expirySeconds) => {
  const expires = new Date();
  expires.setTime(expires.getTime() + expirySeconds * 1000);
  document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/; secure; samesite=Lax`;
};

export default function AuthPage() {
  const params = new URLSearchParams(window.location.search);
  const response_type = params.get("response_type");
  const scope = params.get("scope");
  const client_id = params.get("client_id");
  const redirect_uri = params.get("redirect_uri");

  const [isRegister, setIsRegister] = useState(false);
  
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
          session: browser_session
        });

        console.log("Response from auto-authentication:", response.data);
        
        const {
            authentication_code: authorization_code,
            redirect_uri: n_redirect_uri,
            browser_session: new_browser_session,
            browser_session_exp
        } = response.data;
        
        // Cập nhật lại session nếu server trả về session mới (refresh token)
        if (new_browser_session) {
          const expiry = 3600*24*7;
          setSessionCookie("browser_session", new_browser_session, expiry);
          setSessionCookie("browser_session_exp", browser_session_exp, expiry);
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

  // ---------------------------
  // LOGIN STATES
  // ---------------------------
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [usernameError, setUsernameError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);

  // ---------------------------
  // REGISTER STATES
  // ---------------------------
  const [form, setForm] = useState({
    username: "",
    password: "",
    fullname: "",
    email: "",
    phone: "",
  });

  const [regSuccess, setRegSuccess] = useState("");
  const [regError, setRegError] = useState("");

  const handleRegisterChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ---------------------------
  // SUBMIT REGISTER
  // ---------------------------
  async function handleRegister(e) {
    e.preventDefault();
    setRegError("");
    setRegSuccess("");

    try {
      const res = await axios.post(`${apiUrl}/auth/register`, form);
      setRegSuccess("Đăng ký thành công!");
    } catch (err) {
      setRegError(err.response?.data?.error_description || "Lỗi đăng ký");
    }
  }

  // ---------------------------
  // SUBMIT LOGIN
  // ---------------------------
  async function handleLogin(e) {
    e.preventDefault();

    try {
      const response = await axios.post(`${apiUrl}/auth/authenticate`, {
        response_type,
        scope,
        client_id,
        redirect_uri,
        username,
        password,
      });

      const { authentication_code, redirect_uri: ruri, browser_session } =
        response.data;

      if (browser_session)
        setSessionCookie("browser_session", browser_session, 3600 * 24 * 7);

      window.location.href = `${ruri}?code=${authentication_code}`;
    } catch (error) {
      if (error.response) {
        const errCode = error.response.data.error;
        if (errCode === "wrong_username") {
          setUsernameError(true);
          setPasswordError(false);
        } else if (errCode === "wrong_password") {
          setPasswordError(true);
          setUsernameError(false);
        }
      }
    }
  }

  // =====================================================================
  // JSX RETURN
  // =====================================================================
  return (
    <div className="bg-white p-12 w-5/12">
      {/* Header */}
      <div className="flex items-center text-blue-900 mb-6">
        <img src={logo} alt="HCMUT Logo" className="w-10 h-10 mr-3" />
        <div className="flex flex-col">
          <strong className="text-2xl font-bold">HCMUT SSO</strong>
          <span className="text-sm font-semibold text-blue-700">by OIDC</span>
        </div>
      </div>

      {/* Title */}
      <h2 className="text-3xl font-bold text-blue-900 mb-6 text-center">
        {isRegister ? "Đăng ký tài khoản" : "Đăng nhập"}
      </h2>

      {/* ---------------------------------------------------------- */}
      {/*                REGISTER FORM                               */}
      {/* ---------------------------------------------------------- */}
      {isRegister ? (
        <form onSubmit={handleRegister} className="space-y-4">
          <input
            type="text"
            name="username"
            placeholder="Tên tài khoản"
            className="w-full border p-3 rounded-lg"
            value={form.username}
            onChange={handleRegisterChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Mật khẩu"
            className="w-full border p-3 rounded-lg"
            value={form.password}
            onChange={handleRegisterChange}
            required
          />

          <input
            type="text"
            name="fullname"
            placeholder="Họ và tên"
            className="w-full border p-3 rounded-lg"
            value={form.fullname}
            onChange={handleRegisterChange}
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            className="w-full border p-3 rounded-lg"
            value={form.email}
            onChange={handleRegisterChange}
            required
          />

          <input
            type="text"
            name="phone"
            placeholder="Số điện thoại"
            className="w-full border p-3 rounded-lg"
            value={form.phone}
            onChange={handleRegisterChange}
            required
          />

          {regError && <p className="text-red-600">{regError}</p>}
          {regSuccess && <p className="text-green-600">{regSuccess}</p>}

          <button className="w-full bg-blue-900 text-white py-3 rounded-lg">
            Đăng ký
          </button>

          <p className="text-center mt-4">
            Đã có tài khoản?{" "}
            <span
              onClick={() => setIsRegister(false)}
              className="text-blue-700 cursor-pointer underline"
            >
              Đăng nhập
            </span>
          </p>
        </form>
      ) : (
        /* ---------------------------------------------------------- */
        /*                LOGIN FORM                                  */
        /* ---------------------------------------------------------- */
        <form onSubmit={handleLogin} className="space-y-5">
          <input type="hidden" name="response_type" value={response_type} />
          <input type="hidden" name="scope" value={scope} />
          <input type="hidden" name="client_id" value={client_id} />
          <input type="hidden" name="redirect_uri" value={redirect_uri} />

          <div className="flex flex-col">
            <label className="font-semibold">Tên tài khoản</label>
            <input
              type="text"
              className={`px-4 py-3 rounded-lg bg-blue-50 ${
                usernameError ? "border border-red-500" : ""
              }`}
              value={username}
              required
              onChange={(e) => {
                setUsername(e.target.value);
                setUsernameError(false);
              }}
            />
            {usernameError && (
              <span className="text-red-600">Tên đăng nhập sai</span>
            )}
          </div>

          <div className="flex flex-col">
            <label className="font-semibold">Mật khẩu</label>
            <input
              type="password"
              className={`px-4 py-3 rounded-lg bg-blue-50 ${
                passwordError ? "border border-red-500" : ""
              }`}
              value={password}
              required
              onChange={(e) => {
                setPassword(e.target.value);
                setPasswordError(false);
              }}
            />
            {passwordError && (
              <span className="text-red-600">Mật khẩu sai</span>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-blue-900 text-white py-3 rounded-lg"
          >
            Đăng nhập
          </button>

          <p className="text-center mt-4">
            Chưa có tài khoản?{" "}
            <span
              onClick={() => setIsRegister(true)}
              className="text-blue-700 cursor-pointer underline"
            >
              Đăng ký
            </span>
          </p>
        </form>
      )}
    </div>
  );
}
