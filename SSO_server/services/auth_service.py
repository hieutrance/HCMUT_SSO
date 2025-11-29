import jwt
from jwt import InvalidTokenError
from db import execute_sql, get_connection
from utils.security import hash_password, verify_password
from http import HTTPStatus
from flask import jsonify
from db import execute_sql
import datetime
from flask import request, jsonify
from flask import jsonify
from utils.helpers import  generate_id_token, validate_client_assertion, is_valid_exp, generate_access_token, generate_refresh_token 
import base64, secrets
from datetime import datetime, timezone, timedelta

def register_user(req):
    body_data = req.get_json()
    username = body_data.get("username")
    password = body_data.get("password")
    fullname = body_data.get("fullname")
    email = body_data.get("email", "")
    phone = body_data.get("phone", "")
    address = body_data.get("address", "")

    print(f'''### NEW USER #### \nusername: {username}; password: {password}; fullname: {fullname}; email: {email}; phone: {phone}; address: {address} ''')

    user = execute_sql(
        "SELECT * FROM users WHERE username=%s",
        (username,),
        fetch_one=True
    )
    if user:
        return jsonify({"status": "fail", "msg": "Existed username"}), HTTPStatus.BAD_REQUEST

    hashed = hash_password(password)
    new_user = execute_sql(
        "INSERT INTO users (username, password, fullname, email, phone, address) VALUES (%s,%s,%s,%s,%s,%s)",
        (username, hashed, fullname, email, phone,address)
    )
    return jsonify({"status": "success", "msg": "Successully saved new user"}), HTTPStatus.CREATED

def authorization(req):
    required_params = ["scope", "response_type", "client_id", "redirect_uri", "username", "password"]
    request_data = req.get_json()
    

    username, password = request_data.get("username"), request_data.get("password"),

    scope, response_type, client_id, redirect_uri, nonce = request_data.get("scope"), request_data.get("response_type"), request_data.get("client_id"), request_data.get("redirect_uri"), request_data.get("nonce")
    
    print(f"Redirect URI: {redirect_uri}")
    
    state = request_data.get("state", "")
    
    print(f"username: {username}, response_type: {response_type}, client_id: {client_id}, redirect_uri: {redirect_uri}, nonce: {nonce}, state: {state}")
    
    ## Validate request parameters
    missing = [p for p in required_params if not request_data.get(p)]
    
    print(f"Missing param: {missing}")
    
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
    print(f"Client: {client}")
    if not client:
        return jsonify({
            "error": "not_found_client",
            "error_description": "Not found client"
        }), HTTPStatus.BAD_REQUEST
    
    reidrectUris = execute_sql("SELECT * FROM client_uri WHERE client_id=%s", (client["id"],), False, True)
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
            
        if not verify_password(password, user["password"]):
            return jsonify({
                "error": "wrong_password",
                "error_description": "Wrong password"
            }), HTTPStatus.BAD_REQUEST
            
        authentication_code = secrets.token_urlsafe(32)
        exp_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        temp = execute_sql(
            "INSERT INTO authorization_codes(code, client_id, user_id, redirect_uri, scope, expires_at) VALUES (%s,%s,%s,%s,%s,%s)",
            (authentication_code, client["id"], user["id"], redirect_uri, scope, exp_at)
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

def exchange_token(req):
    req_body = req.get_json()
    required_params = ["client_assertion_type", "client_assertion", "code", "grant_type", "redirect_uri"]
    missing = [p for p in required_params if not req_body.get(p)]
    if len(missing) > 0: 
        return jsonify({
            "error": "bad_request",
            "error_description": f"Required {''.join(missing)} in request body" 
        }), HTTPStatus.BAD_REQUEST
    
    client_assertion_type, client_assertion = req_body.get("client_assertion_type"), req_body.get("client_assertion")
    
    result, info = validate_client_assertion(client_assertion_type, client_assertion)
    # Nếu fails -> result: jsonify(), status code
    if result is not True:
        return result, info
    
    # Nếu success -> result=True, info=payload
    payload = info
    client_id = payload["iss"]
    
    authorization_code = req_body.get("code")
    redirect_uri = req_body.get("redirect_uri")
    grant_type = req_body.get("grant_type")
    
    if not authorization_code or not redirect_uri:
        return jsonify({
            "error": "missing_parameters",
            "error_description": "Missing requried parameters"
        }), HTTPStatus.BAD_REQUEST
        
    db_authorization_code = execute_sql( "SELECT * FROM authorization_codes WHERE code=%s", (authorization_code,), True)
    
    if not db_authorization_code:
        return jsonify({
            "error": "invalid_authorization_code",
            "error_description": "Invalid authorization_code"
        }), HTTPStatus.BAD_REQUEST
    
    now = datetime.utcnow()
    if db_authorization_code["expires_at"] < now:
        return jsonify({
            "error": "invalid_authorization_code",
            "error_description": "Expired authorization code"
        }), HTTPStatus.BAD_REQUEST
    
    print(f'''Expected redirect_uri {db_authorization_code["redirect_uri"]}''')
    
    if redirect_uri != db_authorization_code["redirect_uri"]:
        return jsonify({
            "error": "invalid_redirect_uri",
            "error_description": "Invalid redirect_uri"
        }), HTTPStatus.BAD_REQUEST       
            
    print(f'''Used value: {db_authorization_code["used"]}''')
    if db_authorization_code["used"] == 1:
        return jsonify({
            "error": "invalid_authorization_code",
            "error_description": "Used authorization code"
        }), HTTPStatus.BAD_REQUEST
    # Marked authorization code as used
    checked = execute_sql("UPDATE authorization_codes SET used=True WHERE code=%s", (authorization_code, ))
    if not checked: return jsonify({
        "error": "internal_error",
        "error_description": "Internal server error"
    }), HTTPStatus.INTERNAL_SERVER_ERROR
    
    # Generate idtoken, accesstoken, refreshtoken
    user_id = db_authorization_code["user_id"]
    client_id = db_authorization_code["client_id"]
    
    conn = get_connection()
    cursor = conn.cursor()  
    try:
        id_token = generate_id_token(user_id, client_id)

        # Insert access token
        access_token = secrets.token_urlsafe(32)
        access_exp = (datetime.now(timezone.utc) + timedelta(minutes=10)).replace(tzinfo=None)
        cursor.execute(
            """INSERT INTO access_tokens(token, client_id, user_id, scope, expires_at, revoked)
            VALUES(%s,%s,%s,%s,%s,%s)""",
            (access_token, client_id, user_id, "openid profile", access_exp, False)
        )

        # Insert refresh token
        refresh_token = secrets.token_urlsafe(32)
        refresh_exp = (datetime.now(timezone.utc) + timedelta(days=1)).replace(tzinfo=None)
        cursor.execute(
            """INSERT INTO refresh_tokens(token, client_id, user_id, expires_at, revoked)
            VALUES(%s,%s,%s,%s,%s)""",
            (refresh_token, client_id, user_id, refresh_exp, False)
        )

        # Insert session
        cursor.execute(
            """INSERT INTO user_sessions(id_token, access_token, refresh_token)
            VALUES (%s,%s,%s)""",
            (id_token, access_token, refresh_token)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("DB error:", e)
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        cursor.close()
        conn.close()
        
    
    response_data = {
        "token_type": "Bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 36000,
        "id_token": id_token
    }
    
    response = jsonify(response_data)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    
    return response, HTTPStatus.OK
    
## Check token expiration
def check_token_expiration(req):
    token_type = req.args.get("type")
    token = req.args.get("token")
    
    if not token_type or not token:
        return jsonify({
            "error": "miss_required_parameters",
            "error_description": "Missing required parameters"
        }), HTTPStatus.BAD_REQUEST
        
    if token_type.lower() not in ["access_token", "refresh_token"]:
         return jsonify({
            "error": "unsupported_type",
            "error_desription": "Unsuppoted type"
        }), HTTPStatus.BAD_REQUEST
    else:
        if token_type.lower() == "access_token":
            saved_token = execute_sql('''
                    SELECT * FROM access_tokens 
                    WHERE token=%s                      
                ''', (token,), True)
        else:
            saved_token = execute_sql('''
                    SELECT * FROM refresh_tokens 
                    WHERE token=%s                      
                ''', (token,), True)
            
        if not saved_token:
            return jsonify({
                "error": "invalid_token",
                "error_description": "invalid_token"
            }), HTTPStatus.BAD_REQUEST
            
        if saved_token.expires_at < datetime.now(timezone.utc):
            return jsonify({
                "active": True,
                "client_id": saved_token.client_id,
                "user_id": saved_token.user_id,
                "exp": saved_token.expires_at
            }), HTTPStatus.OK
        else: 
            return jsonify({
                "active": False,
                "client_id": saved_token.client_id,
                "user_id": saved_token.user_id,
                "exp": saved_token.expires_at
            }), HTTPStatus.OK
    
def get_user_info(req):
    auth_header = req.headers.get("Authorization")
    if not auth_header:
        return jsonify({
            "error": "unauthorized",
            "error_description": "Unauthorized"
        }), HTTPStatus.UNAUTHORIZED
        
    token = auth_header.split(" ")[1]
    saved_token = execute_sql(''' 
                SELECT * FROM access_tokens 
                WHERE token=%s                 
            ''', (token,), True)
    
    if saved_token is False:
        return jsonify({
            "error": "interanl_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    if saved_token is None:
        return jsonify({
            "error": "unauthorized",
            "error_description": "Unauthorized"
        }), HTTPStatus.UNAUTHORIZED
    expires_at = saved_token["expires_at"].replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc) or saved_token["revoked"]:
        return jsonify({
            "error": "unauthorized",
            "error_description": "expired token"
        }), HTTPStatus.UNAUTHORIZED

    user_id = saved_token["user_id"]
    scopes = saved_token["scope"].split()
    
    user = execute_sql('''
            SELECT * FROM users 
            WHERE id=%s           
        ''', (user_id, ), True)
    
    if not user: 
        return jsonify({
            "error": "interanl_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    
    response_data = {}
    response_data["sub"] = user_id 
    if "profile" in scopes:
        response_data["username"] = user["username"]
        response_data["fullname"] = user["fullname"]
        response_data["avatar"] = user["avatar"]
    if "email" in scopes:
        response_data["email"] = user["email"]
    if "address" in scopes:
        response_data["address"] = user["address"]
        
    return jsonify(response_data), HTTPStatus.ACCEPTED

def refresh_token(req):
    req_data = req.get_json()
    required_params = ["grant_type", "redirect_uri", "refresh_token", "client_assertion_type", "client_assertion"]
    missing = [p for p in required_params if not req_data.get(p)]
    
    if len(missing) > 0:
        return jsonify({
            "error": "bad_request",
            "error_description": f"Required {' '.join(missing)} in request body"
        }), HTTPStatus.BAD_REQUEST
        
    grant_type = req_data.get("grant_type")
    redirect_uri = req_data.get("redirect_uri")
    refresh_token =  req_data.get("refresh_token")
    client_assertion_type = req_data.get("client_assertion_type")
    client_assertion = req_data.get("client_assertion")
    
    if grant_type != "refresh_token":
        return jsonify({
            "error": "unsupported_grant_type",
            "error_description": "Unsupported grant type"
        }), HTTPStatus.BAD_REQUEST
    
    ## Validate assertion - authorization of client
    result, info = validate_client_assertion(client_assertion_type, client_assertion)
    if result is not True:
        # fail => result: error_msg; info: statu
        # s code
        return result, info
    
    ## Validate client, redirect_uri, refresh_token
    payload = info
    client_id = payload["iss"]
    
    client = execute_sql(''' 
                SELECT * FROM clients
                WHERE id=%s            
            ''', (client_id, ), True)
    
    if client is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    if client is None:
        return jsonify({
            "error": "invalid_client", 
            "error_description": "Not found client"
        }), HTTPStatus.NOT_FOUND

    client_uri_list = execute_sql('''
                SELECT * FROM client_uri
                WHERE client_id=%s                 
            ''', (client_id, ),False, True)
    redirect_uris = [p["redirect_uri"] for p in client_uri_list]
    
    print(f"Expected redirect_uris: {redirect_uris}")
    print(f"Redirect_uri {redirect_uri}")

    if redirect_uri not in redirect_uris:
        return jsonify({
            "error": "invalid_redirect_uri",
            "error_description": "Unaccepted redirect uri"
        }), HTTPStatus.BAD_REQUEST
        
    saved_token = execute_sql(''' 
                SELECT * FROM refresh_tokens
                WHERE token=%s AND client_id=%s
            ''', (refresh_token, client_id), True)
    
    if saved_token is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server erro"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    if saved_token is None:
        return jsonify({
            "error": "invalid_refresh_token",
            "error_description": "Not found refresh token"
        }), HTTPStatus.BAD_REQUEST
    print(f"### Saved token: {saved_token}")    
    
    if saved_token["revoked"] == "1":
        return jsonify({
            "error": "invalid_token",
            "error_description": "Expired refresh token"
        }), HTTPStatus.BAD_REQUEST
    
    if not is_valid_exp(saved_token["expires_at"]):
        return jsonify({
            "error": "expired_token",
            "error_description": "Expired refresh token"
        }), HTTPStatus.BAD_REQUEST
        
    user_id = saved_token["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()  
    try:
        new_id_token = generate_id_token(user_id, client_id)

        # Insert access token
        new_access_token = secrets.token_urlsafe(32)
        new_access_exp = (datetime.now(timezone.utc) + timedelta(minutes=10)).replace(tzinfo=None)
        cursor.execute(
            """INSERT INTO access_tokens(token, client_id, user_id, scope, expires_at, revoked)
            VALUES(%s,%s,%s,%s,%s,%s)""",
            (new_access_token, client_id, user_id, "openid profile", new_access_exp, False)
        )

        # Insert refresh token
        new_refresh_token = secrets.token_urlsafe(32)
        new_refresh_exp = (datetime.now(timezone.utc) + timedelta(days=1)).replace(tzinfo=None)
        cursor.execute(
            """INSERT INTO refresh_tokens(token, client_id, user_id, expires_at, revoked)
            VALUES(%s,%s,%s,%s,%s)""",
            (new_refresh_token, client_id, user_id, new_refresh_exp, False)
        )

        # Insert session
        cursor.execute(
            """INSERT INTO user_sessions(id_token, access_token, refresh_token)
            VALUES (%s,%s,%s)""",
            (new_id_token, new_access_token, new_refresh_token)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("DB error:", e)
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server error"
        }), HTTPStatus.INTERNAL_SERVER_ERROR

    finally:
        cursor.close()
        conn.close()
    
    response_data = {
        "token_type": "Bearer",
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "expires_in": 36000,
        "id_token": new_id_token
    }
    
    response = jsonify(response_data)
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    
    return response, HTTPStatus.OK


def revoke_token(req):
    req_body = req.get_json()
    required_params = ["id_token", "redirect_id"]
    
    missing = [p for p in required_params if not req_body[p]]
    if len(missing) > 0:
        return jsonify({
            "error": "bad_request",
            "error_description": f"Requires {' '.join(missing)} in request body"
        }), HTTPStatus.BAD_REQUEST
    
    id_token = req_body["id_token"]
    payload = jwt.decode(id_token, options={"verify_signature": False})
    
    found_session = execute_sql(''' 
                SELECT * FROM user_sessions
                WHERE id_token=%s                    
            ''', (id_token, ), True)
    
    if found_session is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server erroR"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
    if found_session is None:
        return jsonify({
            "error": "invalid_id_token", 
            "error_description": "Not found id_token"
        }), HTTPStatus.BAD_REQUEST
        
    access_token = found_session["access_token"]
    refresh_token =  found_session["refresh_token"]
        
    ## Accepted: revoke refresh_token and access_token
    check1 = execute_sql(''' 
                UDPATE access_tokens
                SET revoked=True
                WHERE token=%s            
            ''', (access_token,))
    check2 = execute_sql(''' 
                UDPATE refresh_tokens
                SET revoked=True
                WHERE token=%s            
            ''', (refresh_token,))
    
    if check1 is False or check2 is False:
        return jsonify({
            "error": "internal_error",
            "error_description": "Internal server erroR"
        }), HTTPStatus.INTERNAL_SERVER_ERROR
        
    return jsonify({
        "msg": "Revoke successfully"
    }), HTTPStatus.ACCEPTED