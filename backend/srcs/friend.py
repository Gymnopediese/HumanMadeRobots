from sqlalchemy.sql import func
from app import app, db
from flask import request, jsonify
import sys
import hashlib

from sqlalchemy import or_

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

class Friend(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user1 = db.Column(db.String(80))
	user2 = db.Column(db.String(80))
	# 0 baned, 1 stranger, 2 friend
	status = db.Column(db.Integer, nullable=False) 
	created_at = db.Column(db.DateTime(timezone=True),
							server_default=func.now())

	def __repr__(self):
		return f'<Friends {self.username}>'

@app.route('/my_friends', methods=['GET'])
@jwt_required()
def my_friends():
	me = get_jwt_identity()["name"]
	_friends = Friend.query.filter(or_(Friend.user1 == me, Friend.user2 == me)).all()
	friends = [{"username": friend.user2} if me == friend.user1 else {"username": friend.user1} for friend in _friends]
	return jsonify(friends)