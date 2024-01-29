from app import app, db, socketio

from flask_socketio import emit

from flask import request, jsonify

from game.TicTacToe import TicTacToe
import sys

from flask_jwt_extended import jwt_required, get_jwt_identity

from copy import deepcopy
import random
import string
from game.Game import Game
from game.GameHub import new_game

games = {}


modes_simple = [
	"player",
 	"robot",
]

modes = [
	"player",
 	"robot",
	"player_robot",
	"robot_player",
]
#robot vs robot, robot vs player, player vs player, player vs robotd
waitlist = {
	"TicTacToe": {
		"player": [],
		"robot": [],
		"player_robot": [],
		"robot_player": [],
    },
}

def get_game(game_id):
	if game_id in games:
		return games[game_id]
	raise Exception({"stderr": "invalid game id"})

def get_game_name(game_name):
	if game_name in Game.GAMES_NAME:
		return game_name
	raise Exception({"stderr": "invalid game name"})

def get_mode(mode):
	if mode in modes:
		return mode
	raise Exception({"stderr": "invalid mode"})

@app.route('/game/new', methods=['POST'])
@jwt_required()
def create_new_game():
	json = request.get_json()
	if json["game"] == "TicTacToe":
		game = TicTacToe([get_jwt_identity()["name"], "nowon"])
	id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
	games[id] = game
	return jsonify({"game_id": id})

@app.route('/game/waitlist', methods=['POST'])
@jwt_required()
def waitlist():
	game_name = get_game_name(request.get_json()["game"])
	mode = get_mode(request.get_json()["mode"])
	me = "@" if mode.startswith("robot") else "#" + get_jwt_identity()["name"]
	if mode in modes_simple and len(waitlist[game_name][mode]) >= 1:
		players = [me, waitlist[game_name][mode].pop()]
	elif mode == "robot_player" and len(waitlist[game_name]["player_robot"]) >= 1:
		players = [waitlist[game_name]["player_robot"].pop(), me]
	elif mode == "player_robot" and len(waitlist[game_name]["robot_player"]) >= 1:
		players = [me, waitlist[game_name]["robot_player"].pop()]
	else:
		waitlist[game_name][mode].append(me)
		return jsonify({"status": "waiting"})
	game = new_game(game_name, players, False)
	id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
	games[id] = game
	game.send_state()
	return jsonify({"game_id": id})

@app.route('/game/move', methods=['POST'])
@jwt_required()
def move():
	game = get_game(request.headers.get("game_id"))
	game.my_turn(get_jwt_identity()["name"])
	player_move = request.get_json()["move"]
	game.move(player_move)
	game.send_state()
	if game.finished():
		#TODO Save that shit
		return jsonify({"state": game.state(), "winner": game.check_win()})
	return jsonify({"state": game.state()})


# @app.route('/game/bestmove', methods=['POST'])
# @jwt_required()
# def best_move():
# 	if tictactoe.check_win() != 0 or tictactoe.check_draw() == True:
# 		return jsonify({"state": tictactoe.state(), "winner": tictactoe.check_win()})
# 	move = tictactoe.best_move()
# 	print(move, file=sys.stderr)
# 	if tictactoe.move(move) == False:
# 		return jsonify({"status": "invalid move"})
# 	socketio.emit('state',  {"state": tictactoe.state(), "player": tictactoe.player})
# 	return jsonify({"state": tictactoe.state()})

# @app.route('/game/fullgame', methods=['POST'])
# @jwt_required()
# def full_game():
# 	_tictactoe = TicTacToe()
# 	code = request.get_json()
# 	local_scope = {}
 
# 	exec(code["code"], local_scope)
# 	while True:
# 		if _tictactoe.check_win() != 0 or _tictactoe.check_draw() == True:
# 			return jsonify({"state": _tictactoe.state(), "winner": _tictactoe.check_win()})
	
# 		if (code["player"] == 1):
# 			move = local_scope["choose_move"](deepcopy(_tictactoe))
# 			if _tictactoe.move(move) == False:
# 				return jsonify({"status": "invalid move"})
# 			if _tictactoe.check_win() != 0 or _tictactoe.check_draw() == True:
# 				return jsonify({"state": _tictactoe.state(), "winner": _tictactoe.check_win()})
# 			_tictactoe.move(_tictactoe.best_move())
# 		else:
# 			_tictactoe.move(_tictactoe.best_move())
# 			if _tictactoe.check_win() != 0 or _tictactoe.check_draw() == True:
# 				return jsonify({"state": _tictactoe.state(), "winner": _tictactoe.check_win()})
# 			move = local_scope["choose_move"](deepcopy(_tictactoe))
# 			if _tictactoe.move(move) == False:
# 				return jsonify({"status": "invalid move"})

@app.route('/game/state', methods=['GET'])
@jwt_required()
def get_move():
	game = get_game(request.headers.get("game_id"))
	return jsonify({"state": game.state()})