from copy import deepcopy
import sys
import io
import contextlib
from game.AIScript import *
from app import db, app

def get_function(script):
	if "import" in script:
		raise Exception({"stderr": "no import allowed, do not cheat"})
	script = "import random\n" + script
	local_scope = {}
	try:
		exec(script, local_scope)
	except Exception as e:
		raise Exception({"stderr": str(e)})
	if not "choose_move" in local_scope:
		raise Exception({"stderr": "no choose_move function"})
	return local_scope["choose_move"]

class Game:
    
	GAMES_NAME = ["TicTacToe", "Maze", "HighLow"]
    
	GAME_NAME = "none"
    
	def __init__(self) -> None:
		self.storage = {}
    
	def state(self):
		raise Exception({"stderr": "State not implemented"})

	def move(self, move):
		raise Exception({"stderr": "Move not implemented"})

	def check_win(self):
		raise Exception({"stderr": "Check win not implemented"})

	def check_draw(self):
		raise Exception({"stderr": "Check draw not implemented"})

	def possible_moves(self):
		raise Exception({"stderr": "Possible moves not implemented"})

	def best_move(self):
		raise Exception({"stderr": "Best move not implemented"})
    
	def save_script(self, script, username = None, language = "python"):
		with app.app_context():
			_script = AIScript.query.filter_by(game=self.GAME_NAME, user=username).first()
			if not _script:
				_script = AIScript(user=username, language=language, code=script,  game=self.GAME_NAME)
				db.session.add(_script)
			else:
				_script.language = language
				_script.code = script
			db.session.commit()
   
	def send_state(self):
		for player in self.players:
			socketio.emit('state',  {"state": self.state(), "player": self.player}, room=player[1:])
   
	def my_turn(name):
		if name == self.players[self.player][1:]:
			return
		raise Exception({"stderr": "not your turn"})
    
	def exec_script(self, script, username = None, language = "python"):
		
		choose_move = get_function(script)
		output_buffer = io.StringIO()
		copy = deepcopy(self)
		with contextlib.redirect_stdout(output_buffer):
			move = choose_move(copy)
		self.storage = copy.storage
		if not move in self.possible_moves():
			raise Exception({"stderr": "invalid move: " + str(move)})
		captured_output = output_buffer.getvalue()
		self.save_script(script, username, language)
		return {"stdout": captured_output, "move": move}

	def raise_finished(self):
		if self.check_win() != 0 or self.check_draw() == True:
			raise Exception({"state": self.state(), "winner": "game finished"})

	def finished(self):
		return self.check_win() != 0 or self.check_draw()