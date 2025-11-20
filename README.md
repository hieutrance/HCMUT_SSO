**SSO Simulation Project - HCMUT**

A simulation of a Single Sign-On (SSO) system using the OpenID Connect (OIDC) protocol, built with Python Flask. This project demonstrates the interaction between a Service Provider (SP) and an Identity Provider (IdP) in a distributed environment.


🌟 **Features**

Distributed Architecture: Separate Client (SP) and SSO Server (IdP) applications running on different ports.

SSO Login Flow: Redirects unauthenticated users from the Client to the SSO Server for centralized login.

Mock Authentication: Simulates the login process without a real database (for educational purposes).

Cross-Domain Redirects: Demonstrates the redirect flow between localhost:5000 and localhost:5001.

Responsive UI: Clean and modern user interface for Homepage, Login, and Register pages.

Dynamic Backgrounds: Login pages feature a slideshow background script.

🏗️ **Project Structure**

The project follows a microservices-like structure with two distinct Flask applications:

pre>
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



🚀 **Getting Started**

Follow these instructions to set up and run the project on your local machine.

_Prerequisites_

Python 3.x installed.

pip (Python package installer).

_Installation_

Clone the repository:

git clone https://github.com/hieutrance/HCMUT_SSO.git
cd BTL_MMANM


_Create and Activate Virtual Environment:_

**Windows (PowerShell):**

python -m venv .venv
.\.venv\Scripts\Activate


**Linux/macOS:**

python3 -m venv .venv
source .venv/bin/activate


_Install Dependencies:_

pip install Flask requests Flask-CORS PyJWT cryptography


**Running the Application**

You need to run two separate terminals to start both the Client and the Server.

_Terminal 1: Start the Client (Service Provider)_

cd Client
python app.py
Running on http://localhost:5000


_Terminal 2: Start the SSO Server (Identity Provider)_

cd SSO_Server
python app.py
Running on http://localhost:5001


🛠️ **Technologies Used**

Backend: Python, Flask

Frontend: HTML5, CSS3, JavaScript

Security Concepts: SSO, OpenID Connect (OIDC) Flow, Sessions, Cookies

📝 Note

This is a simulation project for the Network Security & Cryptography course. It focuses on the architectural flow of SSO and does not implement full database storage or production-grade encryption mechanisms.


