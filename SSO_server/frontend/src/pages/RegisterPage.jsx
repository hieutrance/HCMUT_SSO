import React from "react";
import RegisterForm from "../components/RegisterForm";
import bg1 from "../assets/bg1.jpg";
import bg2 from "../assets/bg2.jpg";

export default function RegisterPage() {
  return (
    <div className="relative flex items-center justify-center min-h-screen font-sans overflow-hidden">
      {/* Background layer 1 */}
      <div
        className="absolute inset-0 -z-20 bg-cover bg-center"
        style={{ backgroundImage: `url(${bg1})` }}
      ></div>

      {/* Background layer 2 (fade animation) */}
      <div
        className="absolute inset-0 -z-10 bg-cover bg-center opacity-0 animate-fadeSlide"
        style={{ backgroundImage: `url(${bg2})` }}
      ></div>

      {/* Register Form */}
      <RegisterForm />
    </div>
  );
}
