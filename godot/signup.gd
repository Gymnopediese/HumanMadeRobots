extends Node


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _http_request_completed(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print(body.get_string_from_utf8())
	if "token" in res:
		Cookies.save({"token": res["token"]})
		get_tree().change_scene_to_file("res://menu.tscn")

func _on_createaccount_pressed():
	
	var headers = ["Content-Type: application/json"]
	var body = {"username": $name.text, "email":$name.text, "age":23, "password":$name.text, "bio" : "j'aime la nature"}
	
	Utils.post(self, "http://127.0.0.1:5000/signup", self._http_request_completed, headers, body)




