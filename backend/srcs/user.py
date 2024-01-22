from sqlalchemy.sql import func
from app import app, db
from flask import request, jsonify
import sys
import hashlib


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(150), nullable=False)
	age = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(timezone=True),
							server_default=func.now())
	bio = db.Column(db.Text)

	def __repr__(self):
		return f'<Student {self.username}>'

	def __str__(self):
		return f'<Student {self.username}>'


@app.route('/signup', methods=['POST'])
def signup():
	json = request.get_json()
	ename = User.query.filter_by(username=json["username"]).first()
	eemail = User.query.filter_by(email=json["email"]).first()
	if ename:
		return jsonify({"error": "Username already exists"}), 400
	if eemail:
		return jsonify({"error": "Email already exists"}), 400
	password = hashlib.sha512(json["password"].encode()).hexdigest()
	print(password, file=sys.stderr)
	user = User(username= json["username"], password= password, email= json["email"], age= json["age"], bio= json["bio"])
	with app.app_context():
		db.session.add(user)
		db.session.commit()
		token = create_access_token({"name": user.username})
		return jsonify({"username": str(user.username),  "id": str(user.id), "token": token})


@app.route('/signin', methods=['POST'])
def signin():
	json = request.get_json()
	user = User.query.filter_by(username=json["username"]).first()
	password = hashlib.sha512(json["password"].encode()).hexdigest()
	if user is None:
		return jsonify({"error": "User not found"}), 404
	if password != user.password:
		return jsonify({"error": "Invalid password"}), 401
	token = create_access_token({"name": user.username})
	# Return the user data as JSON response
	return jsonify({"username": str(user.username),  "id": str(user.id), "token": token})


@app.route('/me', methods=['GET'])
@jwt_required()
def me():
	user = get_jwt_identity()
	print(user, file=sys.stderr)
	return jsonify(logged_in_as=user), 200

@app.route('/users', methods=['GET'])
@jwt_required()
def users():
	users = User.query.all()
	return jsonify([{"username": str(user.username), "id": str(user.id)} for user in users]), 200
