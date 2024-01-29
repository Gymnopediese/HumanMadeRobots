extends Node2D


var games = [
	{
		"name": "TicTacToe",
	},
	{
		"name": "Maze",
	},
	{
		"name": "HighLow"
	}
]

func goto(game):
	Global.game = game
	get_tree().change_scene_to_file("res://playground/playground.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	var i = 0
	for game in games:
		var game_obj = $game.duplicate()
		game_obj.get_node("name").text = game["name"]
		
		game_obj.get_node("playground").connect("pressed", goto.bind(game["name"]))
		game_obj.position.x += 200 * i
		i += 1
		add_child(game_obj)
	$game.hide()
	print("slaut")
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_button_pressed():
	goto("res://menu.tscn")
