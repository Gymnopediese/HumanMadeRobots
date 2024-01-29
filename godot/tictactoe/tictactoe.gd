extends Node2D

var tiles = []
var client = SocketIOClient

# Called when the node enters the scene tree for the first time.
func _ready():
	for i in range(3):
		tiles.push_back([])
		for j in range(3):
			var sprite = $Sprite2D.duplicate()
			sprite.position = Vector2(100 + i * 150, 100 + j * 150)
			sprite.pressed.connect(click.bind(i, j))
			$board.add_child(sprite)
			tiles[i].push_back(sprite)

func update_state(new_state):
	for y in range(len(new_state)):
		for x in range(len(new_state[y])):
			if new_state[x][y] == 1:
				tiles[x][y].modulate = Color(0, 1, 0)
			elif new_state[x][y] == 2:
				tiles[x][y].modulate = Color(1, 0, 0)
			else:
				tiles[x][y].modulate = Color(0, 0, 0)	

func click(i, j):
	Utils.post(self, "playground/play_move", get_parent().request_completed, [], {"move": [i, j], "game": "TicTacToe"})
