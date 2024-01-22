from sqlalchemy.sql import func
from app import app, db, socketio
from flask import request, jsonify
import sys
import hashlib
from friend import Friend
from user import User
from utils import order_user
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

class Notif(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	from_user = db.Column(db.String(80))
	to_user = db.Column(db.String(80))
	type = db.Column(db.String(150), nullable=False)
	# 0 pending, 1 read, 2 accepted, 3 rejected
	status = db.Column(db.Integer, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True),
							server_default=func.now())

	def __repr__(self):
		return f'<Notifs {self.username}>'

	def __str__(self) -> str:
		return str({"from_user": self.from_user, "to_user": self.to_user, "type": self.type, "status": self.status})

@app.route('/my_notifs', methods=['GET'])
@jwt_required()
def my_notifs():
	me = get_jwt_identity()["name"]
	_notifs = Notif.query.filter_by(to_user=me).all()
	notifs = []
	for notif in _notifs:
		notifs.append({"username": notif.from_user, "type": notif.type, "status": notif.status, "id": notif.id})
	return jsonify(notifs)

@app.route('/send_notif', methods=['POST'])
@jwt_required()
def send_notif():
	json = request.get_json()
	print(json, file=sys.stderr)
	to_user = User.query.filter_by(username=json["to"]).first()
	if to_user is None:
		return jsonify({"error": "User not found"}), 404

	from_user = get_jwt_identity()["name"]
	to_user = json["to"]
 
	notif = Notif(from_user= from_user, to_user=to_user, type= json["type"], status=0)

	print(notif, file=sys.stderr)
	with app.app_context():
		db.session.add(notif)
		db.session.commit()
		socketio.emit('notif',  {"type": json["type"], "from": from_user, "to": to_user, "status":"0", "id": notif.id})
		return jsonify({"type": json["type"]})

@app.route('/respond_notif', methods=['POST'])
@jwt_required()
def respond_notif():
	json = request.get_json()
	me = get_jwt_identity()["name"]
	notif = Notif.query.get(json["id"])

	if notif is None:
		return jsonify({"error": "Notif not found"}), 404
	if notif.to_user != me:
		return jsonify({"error": "Notif not for you"}), 404
 
	notif.status = json["status"]

	# socketio.emit('notif',  {"type": json["type"], "from": from_user, "to": to_user, "status":"0", "id": notif.id})
	with app.app_context():
		db.session.commit()

		if json["status"] != 2:
			return jsonify({"status": "denied"})

		if notif.type == "friend":
			user1, user2 = me, notif.from_user
			friend = Friend(user1= user1, user2=user2, status=1)
			db.session.add(friend)
			db.session.commit()
   
		return jsonify({"status": "ok"})
