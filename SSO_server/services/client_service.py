from db import execute_sql
from flask import jsonify
from http import HTTPStatus
import base64, secrets
from utils.security import hash_password, verify_password

def register_client(req):
    req_body =  req.get_json()
    
    required_params = ["app_name", "app_password"]
    missing = [p for p in required_params if not req_body[p]]
    
    app_name = req_body.get("app_name")
    app_password = req_body["app_password"]
    
    if len(missing) > 0:
        return jsonify({
            "error": "bad_request",
            "error_description": f"Required {' '.join(missing)} in request body"
        }), HTTPStatus.BAD_REQUEST
    
    saved_client = execute_sql(''' 
                SELECT * FROM clients
                WHERE appname=%s                  
            ''', (app_name,), True)
    if saved_client is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
     
    if saved_client is not None:
        return jsonify({
            "error": "invalid_appname",
            "error_description": "Existeed appname"
        }), HTTPStatus.BAD_REQUEST

    hashed_password = hash_password(app_password)
    new_secret = secrets.token_urlsafe(32)  
    temp = execute_sql(''' 
            INSERT INTO clients(appname, apppassword, secretKey)         
            VALUES (%s,%s,%s)
        ''', (app_name, hashed_password, new_secret))
    if temp is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    
    
    return jsonify({
                "msg": "Successfully register"
            }), HTTPStatus.CREATED

def login_client(req):
    req_body = req.get_json()
    required_params = ["app_name","app_password"]
    missing = [p for p in required_params if not req_body[p]]
    if len(missing) > 0:
        return jsonify({
            "error": "invalid_request",
            "error_description": f"Requiered {''.join(missing)} in request's body"
        }), HTTPStatus.BAD_REQUEST
    
    app_name = req_body["app_name"]
    app_password = req_body["app_password"]

    client = execute_sql('''
                SELECT * FROM clients
                WHERE app_name=%s         
            ''', (app_name, ), True)
    if client is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    if client is None:
        return jsonify({
            "error": "wrong_appname",
            "error_description": "Wrong app name"
        }), HTTPStatus.BAD_REQUEST
    if not verify_password(app_password, client["apppassword"]):
        return jsonify({
            "error": "wrong_apppassword",
            "error_description": "Wrong app password"
        }), HTTPStatus.BAD_REQUEST
    
    return jsonify({
        "msg": "Successful login"
    }), HTTPStatus.OK
    