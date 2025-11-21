from flask import Flask
from routes.auth import auth_bp
from routes.users import users_bp
from routes.test import test_bp
app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(test_bp, url_prefix="/api/test" )
if __name__ == "__main__":
    app.run(debug=True)
