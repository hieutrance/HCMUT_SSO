SSO Simulation Project - HCMUT

A simulation of a Single Sign-On (SSO) system using the OpenID Connect (OIDC) protocol, built with Python Flask. This project demonstrates the interaction between a Service Provider (SP) and an Identity Provider (IdP) in a distributed environment.

🌟 Features

Distributed Architecture: Separate Client (SP) and SSO Server (IdP) applications running on different ports.

SSO Login Flow: Redirects unauthenticated users from the Client to the SSO Server for centralized login.

Mock Authentication: Simulates the login process without a real database (for educational purposes).

Cross-Domain Redirects: Demonstrates the redirect flow between localhost:5000 and localhost:5001.

Responsive UI: Clean and modern user interface for Homepage, Login, and Register pages.

Dynamic Backgrounds: Login pages feature a slideshow background script.

🏗️ Project Structure

The project follows a microservices-like structure with two distinct Flask applications:

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

🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

Prerequisites

Python 3.x installed.

pip (Python package installer).

Installation

Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd BTL_MMANM


Create and Activate Virtual Environment:

Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1


Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate


Install Dependencies:

pip install Flask requests Flask-CORS PyJWT cryptography


Running the Application

You need to run two separate terminals to start both the Client and the Server.

Terminal 1: Start the Client (Service Provider)

# Make sure .venv is activated
cd Client
python app.py
# Running on http://localhost:5000


Terminal 2: Start the SSO Server (Identity Provider)

# Make sure .venv is activated
cd SSO_Server
python app.py
# Running on http://localhost:5001


🧪 How to Test

Open your browser and go to http://localhost:5000 (Client Homepage).

You will see the homepage with MyBK and LMS panels.

Click the "Đăng nhập" (Login) button on any panel.

You will be automatically redirected to the SSO Server at http://localhost:5001/login.

Enter any username/password (e.g., admin/admin) and click Login.

You will be redirected back to the Client Homepage.

The button will change to "Truy cập" (Access), and you can now access the LMS and MyBK services.

Click "Đăng xuất" (Logout) to clear the session.

🛠️ Technologies Used

Backend: Python, Flask

Frontend: HTML5, CSS3, JavaScript

Security Concepts: SSO, OpenID Connect (OIDC) Flow, Sessions, Cookies

📝 Note

This is a simulation project for the Network Security & Cryptography course. It focuses on the architectural flow of SSO and does not implement full database storage or production-grade encryption mechanisms.

👥 Authors

[Your Name] - Initial work

Happy Coding! 🚀
