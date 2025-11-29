import React from "react";
import logo from "../assets/logo.png";

export default function LoginForm() {
  return (
    <div className="relative bg-white/85 backdrop-blur-md border border-white/20 shadow-2xl rounded-3xl p-10 w-[90%] max-w-md">
      {/* Header */}
      <div className="flex items-center text-[#003366] mb-6">
        <img src={logo} alt="HCMUT Logo" className="h-10 w-10 mr-3" />
        <div className="flex flex-col leading-tight">
          <strong className="text-2xl font-bold">HCMUT SSO</strong>
          <span className="text-sm font-semibold text-[#0056b3]">by OIDC</span>
        </div>
      </div>

      <h2 className="text-[2.25rem] font-bold text-[#003366] mb-6">Đăng nhập</h2>

      <form className="space-y-5">
        <div>
          <label
            htmlFor="username"
            className="block font-semibold text-gray-800 mb-2 text-[0.95rem]"
          >
            Tên tài khoản
          </label>
          <input
            type="text"
            id="username"
            className="w-full px-4 py-3 bg-[#e6f0fa] rounded-lg text-[#003366] text-base focus:outline-none focus:ring-2 focus:ring-[#0056b3] focus:bg-white"
            required
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="block font-semibold text-gray-800 mb-2 text-[0.95rem]"
          >
            Mật khẩu
          </label>
          <input
            type="password"
            id="password"
            className="w-full px-4 py-3 bg-[#e6f0fa] rounded-lg text-[#003366] text-base focus:outline-none focus:ring-2 focus:ring-[#0056b3] focus:bg-white"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full py-3 bg-[#003366] text-white font-semibold text-lg rounded-lg hover:bg-[#002244] transition-colors"
        >
          Đăng nhập
        </button>
      </form>

      <div className="mt-6 flex flex-col items-center gap-3 text-center">
        <a
          href="forgetpassword.html"
          className="text-[#0056b3] font-semibold hover:underline"
        >
          Quên mật khẩu?
        </a>
        <a
          href="register.html"
          className="text-[#0056b3] font-semibold hover:underline"
        >
          Chưa có tài khoản? Đăng ký
        </a>
      </div>
    </div>
  );
}
