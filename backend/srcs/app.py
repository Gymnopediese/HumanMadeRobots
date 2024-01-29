#!/usr/bin/env python3
from flask import Flask, request
import sys
from flask_jwt_extended import JWTManager, decode_token
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room

from sqlalchemy.sql import func
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Flask
from flask import jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

app = Flask(__name__)

app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=13)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
# app.config["SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]  # Change this!
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")


db = SQLAlchemy(app)


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(days=13))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response



@app.errorhandler(500)
def internal_server_error(e):
    print(e, file=sys.stderr)
    # note that we set the 500 status explicitly
    return "ok", 500


app.register_error_handler(500, internal_server_error)
app.register_error_handler(400, internal_server_error)

@socketio.on('connect')
def test_connect():
	print('Client connected', file=sys.stderr)
 
@socketio.on('joinme')
def test_connect(data):

	me = decode_token(data["token"])["sub"]["name"]
	print('Client join ' + me, file=sys.stderr)
	join_room(me)

import traceback
@app.errorhandler(Exception)
def server_error(err: Exception):
	print(traceback.format_exc(), file=sys.stderr)
	if not type(err.args[0]) is dict:
		return jsonify({"stderr": str(err)}), 200
	app.logger.exception(err.args[0])
	return jsonify(err.args[0]), 200

# emit('connect', {'data': 'Connected'})