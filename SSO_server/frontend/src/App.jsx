import React from "react";
import LoginForm from "./components/LoginForm";
import bg1 from "./assets/bg1.jpg";
import bg2 from "./assets/bg2.jpg";

export default function App() {
  return (
    <div
      className="relative flex items-center justify-center min-h-screen font-sans overflow-hidden"
    >
      {/* Nền 1 */}
      <div
        className="absolute inset-0 -z-20 bg-cover bg-center"
        style={{ backgroundImage: `url(${bg1})` }}
      ></div>

      {/* Nền 2 có hiệu ứng mờ chồng */}
      <div
        className="absolute inset-0 -z-10 bg-cover bg-center opacity-0 animate-fadeSlide"
        style={{ backgroundImage: `url(${bg2})` }}
      ></div>

      {/* Form */}
      <LoginForm />
    </div>
  );
}
