extends Node


var client = SocketIOClient
var backendURL: String

func _ready():
	# prepare URL
	backendURL = "http://localhost:5000/socket.io"
	client = SocketIOClient.new(backendURL, on_socket_event, on_socket_ready, on_socket_connect)
	add_child(client)

func _exit_tree():
	# optional: disconnect from socketio server
	client.socketio_disconnect()

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
	# respond hello world
	client.socketio_send("hello", "world")


func _on_button_pressed():
	client.socketio_send("message", "world")
