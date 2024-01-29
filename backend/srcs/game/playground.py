from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from copy import deepcopy
from app import app, socketio
from game.GameHub import new_game
from flask import request, jsonify
import sys
from flask_jwt_extended import jwt_required, get_jwt_identity
from copy import deepcopy
from game.AIScript import AIScript
from game.Game import get_function
playground = {}

def get_create_game(game_name, name, finished = True):
	if not name + game_name in playground:
		game = new_game(game_name)
		playground[name + game_name] = game
	if finished:
		playground[name + game_name].raise_finished()
	return playground[name + game_name]


@app.route('/playground/new', methods=['POST'])
@jwt_required()
def new_playground():
	json = request.get_json()
	game = new_game(json["game"])
	playground[get_jwt_identity()["name"] + json["game"]] = game
	return jsonify({"state": game.state()})

@app.route('/playground/play_best_move', methods=['POST'])
@jwt_required()
def play_best_move():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"])
	game.move(game.best_move())
	return jsonify({"state": game.state()})

@app.route('/playground/get_best_move', methods=['POST'])
@jwt_required()
def get_best_move():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"])
	return jsonify({"move": game.best_move()})

@app.route('/playground/get_my_best_move', methods=['POST'])
@jwt_required()
def get_my_best_move():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"])
	result = game.exec_script(json["code"], get_jwt_identity()["name"])
	return jsonify(result)

@app.route('/playground/undo_move', methods=['POST'])
@jwt_required()
def undo_move():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"], False)
	game.undo()
	return jsonify({"state": game.state()})

@app.route('/playground/play_move', methods=['POST'])
@jwt_required()
def play_move():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"])
	game.move(json["move"])
	return jsonify({"state": game.state(), "winner": game.check_win()})

@app.route('/playground/exec_ia_script', methods=['POST'])
@jwt_required()
def iamove():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"])
	result = game.exec_script(json["code"], get_jwt_identity()["name"])
	game.move(result["move"])
	result["state"] = game.state()
	return jsonify(result)

@app.route('/playground/upload_ai_script', methods=['POST'])
@jwt_required()
def ai_script():
	json = request.get_json()
	game = get_create_game(json["game"], get_jwt_identity()["name"], False)
	result = game.exec_script(json["code"], get_jwt_identity()["name"])
	return jsonify(result)

@app.route('/playground/get_ai_script', methods=['POST'])
@jwt_required()
def get_ai_script():
	json = request.get_json()
	script = AIScript.query.filter_by(game=json["game"], user=get_jwt_identity()["name"]).first()
	if not script:
		return jsonify({"language": "python", "code": ""})
	return jsonify({"language": script.language, "code": script.code})

@app.route('/playground/get_state', methods=['GET'])
@jwt_required()
def get_state():
	game_name = request.headers.get("game")
	game = get_create_game(game_name, get_jwt_identity()["name"])
	return jsonify({"state": game.state()})

@app.route('/playground/ia_full_game', methods=['POST'])
@jwt_required()
def ia_full_game():
	json = request.get_json()
	if int(json["amount"]) > 100:
		return jsonify({"status": "too many games"})
	choose_move = get_function(json["code"])
	choose_move = choose_move["function"]
	res = [0] * game.PLAYER_AMMOUNT
	for _ in range(int(json["amount"])):
		game = new_game(json["game"])
		while True:
			if game.finished():
				res[game.check_win()] += 1
				break
			if game.player == json["player"]:
				game.move(choose_move(deepcopy(game)))
			else:
				game.move(game.best_move())
	return jsonify({"player1": res[1], "player2": res[2], "draw": res[0]})
from time import sleep

@app.route('/playground/ia_anime_game', methods=['POST'])
@jwt_required()
def ia_anime_game():
	json = request.get_json()
	if int(json["amount"]) > 100:
		return jsonify({"status": "too many games"})
	choose_move = get_function(json["code"])
	sleep_time = 0.2
	game = get_create_game(json["game"], get_jwt_identity()["name"])
	while True:
		app.logger.info("game: " + str(game.state()))
		if game.finished():
			break
		if game.player == json["player"]:
			game.move(choose_move(deepcopy(game)))
		else:
			game.move(game.best_move())
		socketio.emit('state',  {"state": game.state(), "player": game.player}, room=get_jwt_identity()["name"])
		sleep(sleep_time)
	return jsonify({"winner": game.check_win(), "state": game.state()})










# def choose_move(tictactoe):
# 	bot = tictactoe.player
# 	moves = tictactoe.possible_moves()
# 	if len(moves) == 9:
# 		return [0, 0]
# 	best_move = moves[0]
# 	minmax = -2
# 	for	move in moves:
# 		tictactoe.board[move[0]][move[1]] = bot
# 		move_value = rec(tictactoe, (bot % 2) + 1, bot, 0)
# 		if minmax < move_value:
# 			best_move = move
# 			minmax = move_value
# 		tictactoe.board[move[0]][move[1]] = 0
# 	return best_move

# def rec(self, current_player, bot, depth):
# 	winner = self.check_win()
# 	if winner == bot:
# 		return 9 - depth
# 	elif winner != 0:
# 		return -9 + depth
# 	elif self.check_draw():
# 		return 0
# 	if current_player == bot:
# 		minmax = -10
# 	else:
# 		minmax = 10
# 	moves = self.possible_moves()
# 	for	move in moves:
# 		self.board[move[0]][move[1]] = current_player
# 		if (current_player == bot):
# 			minmax = max(minmax, self.rec((current_player) % 2 + 1, bot,  depth + 1))
# 		else:
# 			minmax = min(minmax, self.rec((current_player) % 2 + 1, bot,  depth + 1))
# 		self.board[move[0]][move[1]] = 0
# 	return minmax