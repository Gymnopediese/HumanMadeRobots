from sqlalchemy.sql import func
from app import app, db, socketio
from flask import request, jsonify
import sys
import hashlib
from utils import order_user
from user import User
from sqlalchemy import or_, and_
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	from_user = db.Column(db.String(80))
	to_user = db.Column(db.String(80))
	content = db.Column(db.String(150), nullable=False)
	created_at = db.Column(db.DateTime(timezone=True),
							server_default=func.now())

	def __repr__(self):
		return f'<Student {self.username}>'

	def __str__(self) -> str:
		return str({"from_user": self.from_user, "to_user": self.to_user, "content": self.content})

@app.route('/message', methods=['POST'])
@jwt_required()
def send_message():
	json = request.get_json()
	print(json, file=sys.stderr)
	to_user = User.query.filter_by(username=json["to"]).first()
	if to_user is None:
		return jsonify({"error": "User not found"}), 404

	from_user, to_user = get_jwt_identity()["name"], json["to"]
 
	message = Message(from_user= from_user, to_user=to_user, content= json["content"])

	for user in [from_user, to_user]:
		socketio.emit('message',  {"content": json["content"], "from": from_user, "to": to_user}, room=user)
	with app.app_context():
		db.session.add(message)
		print(message, file=sys.stderr)
		db.session.commit()
		return jsonify({"content": json["content"]})


@app.route('/messages', methods=['GET'])
@jwt_required()
def get_message():
	from_user, to_user = get_jwt_identity()["name"], request.headers.get('to')
	print(from_user, to_user, file=sys.stderr)
	_messages = Message.query.filter(or_(
     	and_(Message.from_user == from_user, Message.to_user == to_user),
      	and_(Message.from_user == to_user, Message.to_user == from_user))).all()
	messages = []
	for message in _messages:
		messages.append(message.content)
	return jsonify({"messages": messages})

# @socketio.on('message')
# def handle_message(data):
#     print('received message: ' + data, file=sys.stderr)
#     socketio.emit("message", "no")

