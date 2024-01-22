extends Node2D

# Called when the node enters the scene tree for the first time.
func _ready():
	Utils.gett(self, "my_notifs", _on_load)

func _friend_request(result, response_code, headers, body):
	print(body.get_string_from_utf8())

func friend_request(id, status):
	Utils.post(self, "respond_notif", _friend_request, [], {"id": id, "status": status})

func _on_load(result, response_code, headers, body):
	print(body.get_string_from_utf8())
	body = JSON.parse_string(body.get_string_from_utf8())
	if (body == null):
		print("rip")
		return
	#$RichTextLabel.text = "Users\n"
	var i = 0
	for user in body:
		var user_obj: Node2D = $notif.duplicate()
		
		user_obj.get_node("username").text = user["username"]
		user_obj.get_node("accept").connect("pressed", friend_request.bind(user["id"], 2))
		user_obj.get_node("deny").connect("pressed", friend_request.bind(user["id"], 3))
		user_obj.position.y = user_obj.position.x + i *100
		i += 1
		add_child(user_obj)
	$notif.hide()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
