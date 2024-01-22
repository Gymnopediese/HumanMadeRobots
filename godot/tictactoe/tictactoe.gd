extends Node2D

var tiles = []
var client = SocketIOClient

# Called when the node enters the scene tree for the first time.
func _ready():
	var backendURL = "http://localhost:5000/socket.io"
	client = SocketIOClient.new(backendURL, on_socket_event, on_socket_ready, on_socket_connect)
	add_child(client)
	for i in range(3):
		tiles.push_back([])
		for j in range(3):
			var sprite = $Sprite2D.duplicate()
			sprite.position = Vector2(100 + i * 200, 100 + j * 200)
			sprite.pressed.connect(click.bind(i, j))
			add_child(sprite)
			tiles[i].push_back(sprite)
	Utils.gett(self, "http://localhost:5000/tictactoe/state", request_completed)

func update_state(new_state):
	for y in range(len(new_state)):
		for x in range(len(new_state[y])):
			if new_state[x][y] == 1:
				tiles[x][y].modulate = Color(0, 1, 0)
			elif new_state[x][y] == 2:
				tiles[x][y].modulate = Color(1, 0, 0)
			else:
				tiles[x][y].modulate = Color(0, 0, 0)	

func request_completed(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print(body.get_string_from_utf8())
	if res == null:
		print("rquest error")
		return
	if "stdout" in res:
		$consol.text = res["stdout"]
	if "state" in res:
		update_state(res["state"])
	else:
		print("invalid state")

func click(i, j):
	Utils.post(self, "http://localhost:5000/tictactoe/move", request_completed, [], {"move": [i, j]})



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_reset_pressed():
	Utils.post(self, "http://localhost:5000/tictactoe/new", request_completed)


func on_socket_ready(_sid: String):
	# connect to socketio server when engine.io connection is ready
	client.socketio_connect()

func on_socket_connect(_payload: Variant, _name_space, error: bool):
	if error:
		push_error("Failed to connect to backend!")
	else:
		print("Socket connected")

func on_socket_event(event_name: String, payload: Variant, _name_space):
	print("Received ", event_name, " ", payload)
	
	print(event_name)
	if event_name != "state":
		return
		
	update_state(payload["state"])
	
	


func _on_iamove_pressed():
	Utils.post(self, "http://localhost:5000/tictactoe/iamove", request_completed, [], {"code": $TextEdit.text})


func _on_bestmove_pressed():
	Utils.post(self, "http://localhost:5000/tictactoe/bestmove", request_completed);


func _on_play_ai_pressed():
	Utils.post(self, "http://localhost:5000/tictactoe/fullgame", request_completed, [], {"code": $TextEdit.text, "player": 1})


func _on_play_ai_2_pressed():
		Utils.post(self, "http://localhost:5000/tictactoe/fullgame", request_completed, [], {"code": $TextEdit.text, "player": 2})
