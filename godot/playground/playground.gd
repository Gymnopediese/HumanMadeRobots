extends Node2D

var tiles = []
var client = SocketIOClient

@export var game = "TicTacToe"

var files = {
	"TicTacToe": "res://tictactoe/tictactoe.tscn",
	"Maze": "res://maze/maze.tscn",
	"HighLow": "res://highlow/highlow.tscn",
}

# Called when the node enters the scene tree for the first time.
func _ready():
	if Global.game != "":
		game=  Global.game
	var game_obj = load(files[game]).instantiate()
	game_obj.name = "game"
	add_child(game_obj)
	Utils.post(self, "playground/get_ai_script", _put_script, [], {"game": game})
	var backendURL = "http://localhost:5000/socket.io"
	client = SocketIOClient.new(backendURL, _on_socket_event)
	add_child(client)
	Utils.gett(self, "playground/get_state", request_completed, ["game: " + game])

func _put_script(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	$playground/code.text = res["code"]

func request_completed(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print(body.get_string_from_utf8())
	if res == null:
		print("rquest error")
		return
	if "stdout" in res and res["stdout"]:
		$playground/consol.text += "stdout:\n" + res["stdout"] + '\n'
	if "stderr" in res and res["stderr"]:
		$playground/consol.text += "Error:\n" + res["stderr"] + "\n"
	if "state" in res:
		$game.update_state(res["state"])
	else:
		print("invalid state")
	$playground/consol.scroll_vertical = 1000000

func _on_reset_pressed():
	Utils.post(self, "playground/new", request_completed, [], {"game": game})

func _on_socket_event(event_name: String, payload: Variant, _name_space):
	if event_name != "state":
		return
	$game.update_state(payload["state"])

func _on_iamove_pressed():
	Utils.post(self, "playground/exec_ia_script", request_completed, [], {"code": $playground/code.text, "language": "python", "game": game})

func _on_bestmove_pressed():
	Utils.post(self, "playground/play_best_move", request_completed, [], {"game": game});

func _on_play_ai_pressed():
	Utils.post(self, "playground/ia_anime_game", request_completed, [], {"code": $playground/code.text, "player": 1, "amount": $playground/slider.value, "game": game})	
	#Utils.post(self, "http://localhost:5000/ia_full_game", request_completed, [], {"code": $TextEdit.text, "player": 1, "amount": $slider.value})

func _on_h_slider_value_changed(value):
	$playground/slider/RichTextLabel.text = str(value)

func _print_best_move(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print(body.get_string_from_utf8())
	print($playground/consol.scroll_vertical)
	if "stdout" in res and res["stdout"]:
		$playground/consol.text += "stdout:\n" + res["stdout"] + "\n"
	if "stderr" in res and res["stderr"]:
		$playground/consol.text += "Error:\n" + res["stderr"] + "\n"
	if "move" in res:
		$playground/consol.text += "the best move is " + str(res["move"]) + "\n"
	$playground/consol.scroll_vertical = 1000000

func _on_printbestmove_pressed():
	Utils.post(self, "playground/get_best_move", _print_best_move, [], {"game": game});


func _on_printmybestmove_pressed():
	Utils.post(self, "playground/get_my_best_move", _print_best_move, [], {"game": game, "code": $playground/code.text, "language": "python"});


func _on_undo_pressed():
	Utils.post(self, "playground/undo_move", request_completed, [], {"game": game});


func _on_back_pressed():
	get_tree().change_scene_to_file("res://game/games.tscn")


func _on_play_anime_pressed():
	Utils.post(self, "playground/ia_anime_game", request_completed, [], {"code": $playground/code.text, "player": 2, "amount": $playground/slider.value, "game": game})
