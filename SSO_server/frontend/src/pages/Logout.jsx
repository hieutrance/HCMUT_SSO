import Cookies from "js-cookie";
import { useState, useEffect } from "react";
import LoadingSpinner from "../components/LoadingSpinner";
import logo from "../assets/images/logo.png";
import axios from "axios";
const apiUrl = "http://localhost:5001/api";


function getCookie(name) {
  const value = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="));
  return value ? value.split("=")[1] : null;
}


export default function LogoutPage() {
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const redirect = params.get("redirect");

    const allCookies = Cookies.get();
    let browser_session = getCookie("browser_session")
    Object.keys(allCookies).forEach((cookieName) => {
      Cookies.remove(cookieName, { path: "/" });
    });
    
    try {
      setIsLoading(true);
      const response = axios.post(`${apiUrl}/auth/revoke`, {
        "redirect_uri": redirect,
        "browser_session": browser_session
      })
    } catch  (error) {
      console.log("Error in revoking session");
    } finally {
      setIsLoading(false);
    }

    if (redirect) {
      window.location.href = redirect;
    } else {
      window.location.href = "/login";
    }
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center  px-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 max-w-md w-full text-center">
        <div className="flex flex-col items-center mb-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-16 w-16 text-red-500 mb-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H6a2 2 0 01-2-2V7a2 2 0 012-2h5a2 2 0 012 2v1"
            />
          </svg>
        </div>

        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          Bạn đã đăng xuất
        </h1>

        <p className="text-gray-600 mb-6">
          Phiên đăng nhập của bạn đã kết thúc. Hẹn gặp lại bạn lần sau nhé!
        </p>
      </div>
    </div>
  );
}
