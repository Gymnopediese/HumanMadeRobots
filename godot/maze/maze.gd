extends Node2D

var tiles = []

func _ready():
	for i in range(11):
		tiles.push_back([])
		for j in range(11):
			var sprite = $tile.duplicate()
			sprite.position = Vector2(100 + i * 50, 100 + j * 50)
			$board.add_child(sprite)
			tiles[i].push_back(sprite)

func _process(delta):
	if Input.is_action_just_pressed("ui_up"):
		Utils.post(self, "playground/play_move", get_parent().request_completed, [], {"move": 0, "game": "Maze"})

	if Input.is_action_just_pressed("ui_right"):
		Utils.post(self, "playground/play_move", get_parent().request_completed, [], {"move": 1, "game": "Maze"})

	if Input.is_action_just_pressed("ui_down"):
		Utils.post(self, "playground/play_move", get_parent().request_completed, [], {"move": 2, "game": "Maze"})

	if Input.is_action_just_pressed("ui_left"):
		Utils.post(self, "playground/play_move", get_parent().request_completed, [], {"move": 3, "game": "Maze"})


func update_state(new_state):
	var board = new_state["board"]
	var pos = new_state["position"]
	for y in range(len(board)):
		for x in range(len(board[y])):
			if board[x][y] == 1:
				tiles[x][y].modulate = Color(0, 1, 0)
			elif board[x][y] == 2:
				tiles[x][y].modulate = Color(0, 0, 1)
			else:
				tiles[x][y].modulate = Color(0, 0, 0)	
	tiles[pos[0]][pos[1]].modulate = Color(1, 0, 0)
