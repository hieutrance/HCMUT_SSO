from db import execute_sql
from utils.security import hash_password, verify_password
import datetime
from flask import request, jsonify
from http import HTTPStatus
from flask import jsonify
from utils.helpers import create_jwt, verify_jwt

def authorization(data):
    required_params = ["scope", "response_type", "client_id", "redirect_uri", "username", "password"]

    username, password = request.args.get("username"), request.args.get("password"),

    scope, response_type, client_id, redirect_uri, nonce = request.args.get("scope"), request.args.get("response_type"), request.args.get("client_id"), request.args.get("redirect_uri"), request.args.get("nonce")
    
    state = request.args.get("state", "")
    
    ## Validate request parameters
    missing = [p for p in required_params if not request.args.get(p)]
    if missing:
        return jsonify({
            "error": "invalid_request",
            "error_description": f"Missing parameters {', '.join(missing)}"
        }), HTTPStatus.BAD_REQUEST
        
    if "openid" not in scope:
        return jsonify({
            "error": "invalid_scope",
            "error_description": "suppose openid in scope parameter"
        }), HTTPStatus.BAD_REQUEST

    if response_type not in ["code", "id_token token", "token"]:
        return jsonify({
            "error": "unsupported_response_type",
            "error_description": "unsupported response type"
        }), HTTPStatus.BAD_REQUEST

    ## Check client_id and redirect_uri
    client = execute_sql("SELECT * FROM clients WHERE id = %s", (client_id,), True)
    if not client:
        return jsonify({
            "error": "not_found_client",
            "error_description": "Not found client"
        }), HTTPStatus.BAD_REQUEST
    
    reidrectUris = execute_sql("SELECT * FROM client_uri WHERE client_id=%s", (client.id,), False, True)
    print(f"All redirectUris: {reidrectUris}")
    
    if redirect_uri not in redirect_uri:
        return jsonify({
            "error": "invalid_uri",
            "error_description": "Invalid redirect uri, register uri with app"
        }), HTTPStatus.BAD_REQUEST
    else:
        ## Validate user credentials
        user = execute_sql("SELECT * FROM users WHERE username=%s", (username, ), True, False)
        
        if not user:
            return jsonify({
                "error": "wrong_username",
                "error_description": "Wrong username, register first"
            }), HTTPStatus.BAD_REQUEST
            
        if not verify_password(password, user.password):
            return jsonify({
                "error": "wrong_password",
                "error_description": "Wrong password"
            }), HTTPStatus.BAD_REQUEST
            
        authentication_code = create_jwt({
            "client": client.id,
        }, 10)
        exp_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

        temp = execute_sql(
            "INSERT INTO authorization_codes(client_id, user_id, redirect_uri, scope, expires_at) VALUES ()",
            (authentication_code, client.id, redirect_uri, scope, exp_at)
        )
        if not temp:
            return jsonify({
                "error": "internal_error",
                "error_description": "Internal error with db"
            }), HTTPStatus.INTERNAL_SERVER_ERROR     
            
        response_data = {
            "authentication_code": authentication_code,
            "redirect_uri": redirect_uri
        }
        if state: 
            response_data["state"] = state

        return jsonify(response_data), HTTPStatus.OK