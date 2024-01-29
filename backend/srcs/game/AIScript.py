from app import db
from sqlalchemy.sql import func

class AIScript(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(80))
	game = db.Column(db.String(80))
	language = db.Column(db.String(80))
	code = db.Column(db.String(5000))
	created_at = db.Column(db.DateTime(timezone=True),
							server_default=func.now())

	def __repr__(self):
		return f'<Friends {self.user}>'

	def __str__(self) -> str:
		return str({"user": self.user, "game": self.game, "language": self.language, "code": self.code, "created_at": self.created_at})