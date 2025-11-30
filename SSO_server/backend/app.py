from flask import Flask, render_template, request
from routes.auth import auth_bp
from routes.client import client_bp
from routes.test import test_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(client_bp, url_prefix="/api/client")
app.register_blueprint(test_bp, url_prefix="/api/test" )

if __name__ == "__main__":
    app.run(debug=True, port=5001)