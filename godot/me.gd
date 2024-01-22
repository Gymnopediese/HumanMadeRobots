extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass



func _http_request_completed(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print(body.get_string_from_utf8())


func _on_login_pressed():
	
	var headers = ["Content-Type: application/json", "Authorization: Bearer " + $token.text]
	
	Utils.gett(self, "http://127.0.0.1:5000/me", self._http_request_completed, headers)

