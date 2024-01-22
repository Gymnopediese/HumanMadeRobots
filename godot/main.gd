extends Node2D


func me(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
	print(json)
	print("cookie ", Cookies.load())
	print("cookie ", Cookies.load())
	if ("logged_in_as") in json:
		print("YOU ar logged")
		Global.me = json
		get_tree().change_scene_to_file("res://menu.tscn")
	else:
		print("rip")
		$Signup.show()
		$Signin.show()
		
	

func _ready():
	Utils.gett(self, "me", me)

# Called when the HTTP request is completed.
func _http_request_completed(result, response_code, headers, body):
	var json = JSON.new()
	json.parse(body.get_string_from_utf8())
	var response = json.get_data()

	if "token" in json:
		Cookies.save(json["token"])
		print("Token saved")
	print(body.get_string_from_utf8())

func _on_button_pressed():
	var headers = ["Content-Type: application/json"]
	var body = {"code": $TextEdit.text}
	
	Utils.post(self, "http://127.0.0.1:5000/pyexec", self._http_request_completed, headers, body)



func _on_createaccount_pressed():

	var headers = ["Content-Type: application/json"]
	var body = {"firstname":'john', "lastname":'doasdfe', "email":'jadsfd@example.com', "age":23, "bio":'Biology sasdftudent'}
	
	Utils.post(self, "http://127.0.0.1:5000/user", self._http_request_completed, headers, body)

