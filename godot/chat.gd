extends Node2D

var tiles = []
var client = SocketIOClient

var messages = []
# Called when the node enters the scene tree for the first time.
func _ready():
	var backendURL = "http://localhost:5000/socket.io"
	client = SocketIOClient.new(backendURL, on_socket_event)
	add_child(client)
	if (Global.chat_name):
		Utils.gett(self, "http://localhost:5000/messages", request_completed, ["to: " + Global.chat_name])
	else:
		get_tree().change_scene_to_file("res://menu.tscn")

func request_completed(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print("recieved: ", body.get_string_from_utf8())
	if (res == null):
		print("invalid response")
		return
	if "messages" in res:
		messages = res["messages"]
		$consol.text = "\n".join(messages)




func on_socket_event(event_name: String, payload: Variant, _name_space):
	print("Received ", event_name, " ", payload)
	
	print(event_name)
	if event_name != "message":
		return
		
	messages.push_back(payload["content"])
	$consol.text = "\n".join(messages)
	
func _on_button_pressed():
	Utils.post(self, "http://localhost:5000/message", request_completed, [], {"to": Global.chat_name, "content": $input.text})
	$input.text = ""


func _on_button_2_pressed():
	get_tree().change_scene_to_file("res://menu.tscn")
