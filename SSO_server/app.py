from flask import Flask, render_template, request
from routes.auth import auth_bp
from routes.client import client_bp
from routes.test import test_bp

app = Flask(__name__)


@app.route('/authoriate')
def render_authoration_ui():

    scope = request.args.get("scope")
    response_type = request.args.get("response_type")
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")

    print(scope, response_type, client_id, redirect_uri)

    return render_template('loginpage.html',
                           scope=scope,
                           response_type=response_type,
                           client_id=client_id,
                           redirect_uri=redirect_uri)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(client_bp, url_prefix="/api/client")
app.register_blueprint(test_bp, url_prefix="/api/test" )



if __name__ == "__main__":
    app.run(debug=True)
