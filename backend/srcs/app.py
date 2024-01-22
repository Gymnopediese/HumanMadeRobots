#!/usr/bin/env python3
from flask import Flask, request
import sys
from flask_jwt_extended import JWTManager, decode_token
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room

from sqlalchemy.sql import func

app = Flask(__name__)

app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]  # Change this!
# app.config["SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]  # Change this!
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")


db = SQLAlchemy(app)


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
# emit('connect', {'data': 'Connected'})