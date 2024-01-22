from app import app, db, socketio

from flask_socketio import emit

from flask import request, jsonify

from tictactoe.game import TicTacToe
import sys

from flask_jwt_extended import jwt_required, get_jwt_identity

from copy import deepcopy
import random
import string
tictactoe = TicTacToe(["nowon", "nowon"])

games = {}

waitlist = {
	"TicTacToe": []
}

@app.route('/tictactoe/new', methods=['POST'])
@jwt_required()
def new_game():
	json = request.get_json()
	if json["game"] == "TicTacToe":
		game = TicTacToe([get_jwt_identity()["name"], "nowon"])
	id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
	games[id] = game
	return jsonify({"game_id": id})

@app.route('/tictactoe/waitlist', methods=['POST'])
@jwt_required()
def waitlist():
	game_name = request.get_json()["game"]
	me = get_jwt_identity()["name"]
	waitlist[game_name].append(me)
	if len(waitlist[game_name]) >= 2:
		players = [waitlist[game_name].pop(), waitlist[game_name].pop()]
		game = TicTacToe(players)
		id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
		games[id] = game
		for player in players:
			emit('game', {"game_id": id, "game": game_name, "players": players}, room=player)
		return jsonify({"game_id": id})
	return jsonify({"status": "waiting"})

@app.route('/tictactoe/move', methods=['POST'])
@jwt_required()
def move():
	if tictactoe.check_win() != 0 or tictactoe.check_draw() == True:
		return jsonify({"state": tictactoe.state(), "winner": tictactoe.check_win()})


	player_move = request.get_json()
	if tictactoe.move(player_move["move"]) == False:
		return jsonify({"status": "invalid move"})
	socketio.emit('state',  {"state": tictactoe.state(), "player": tictactoe.player})
	if tictactoe.check_win() != 0:
		return jsonify({"state": tictactoe.state(), "winner": tictactoe.check_win()})
	return jsonify({"state": tictactoe.state()})

import io
import contextlib


@app.route('/tictactoe/iamove', methods=['POST'])
@jwt_required()
def iamove():
	if tictactoe.check_win() != 0 or tictactoe.check_draw() == True:
		return jsonify({"state": tictactoe.state(), "winner": tictactoe.check_win()})


	code = request.get_json()
	local_scope = {}
	exec(code["code"], local_scope)
 
	output_buffer = io.StringIO()
	# Redirect stdout to the buffer
	with contextlib.redirect_stdout(output_buffer):
		move = local_scope["choose_move"](deepcopy(tictactoe))

	# Get the content of the buffer
	captured_output = output_buffer.getvalue()
	if tictactoe.move(move) == False:
		return jsonify({"status": "invalid move"})
	socketio.emit('state',  {"state": tictactoe.state(), "player": tictactoe.player})
	return jsonify({"state": tictactoe.state(), "stdout": captured_output})

@app.route('/tictactoe/bestmove', methods=['POST'])
@jwt_required()
def best_move():
	if tictactoe.check_win() != 0 or tictactoe.check_draw() == True:
		return jsonify({"state": tictactoe.state(), "winner": tictactoe.check_win()})

	move = tictactoe.best_move()
	print(move, file=sys.stderr)
	if tictactoe.move(move) == False:
		return jsonify({"status": "invalid move"})
	socketio.emit('state',  {"state": tictactoe.state(), "player": tictactoe.player})
	return jsonify({"state": tictactoe.state()})

@app.route('/tictactoe/fullgame', methods=['POST'])
@jwt_required()
def full_game():
	_tictactoe = TicTacToe()
	code = request.get_json()
	local_scope = {}
 
	exec(code["code"], local_scope)
	while True:
		if _tictactoe.check_win() != 0 or _tictactoe.check_draw() == True:
			return jsonify({"state": _tictactoe.state(), "winner": _tictactoe.check_win()})
	
		if (code["player"] == 1):
			move = local_scope["choose_move"](deepcopy(_tictactoe))
			if _tictactoe.move(move) == False:
				return jsonify({"status": "invalid move"})
			if _tictactoe.check_win() != 0 or _tictactoe.check_draw() == True:
				return jsonify({"state": _tictactoe.state(), "winner": _tictactoe.check_win()})
			_tictactoe.move(_tictactoe.best_move())
		else:
			_tictactoe.move(_tictactoe.best_move())
			if _tictactoe.check_win() != 0 or _tictactoe.check_draw() == True:
				return jsonify({"state": _tictactoe.state(), "winner": _tictactoe.check_win()})
			move = local_scope["choose_move"](deepcopy(_tictactoe))
			if _tictactoe.move(move) == False:
				return jsonify({"status": "invalid move"})

@app.route('/tictactoe/state', methods=['GET'])
@jwt_required()
def get_move():
	return jsonify({"state": tictactoe.state()})