extends Node2D

var tiles = []
var client = SocketIOClient
var phase = 0

func update_state(new_state):
	print(new_state)
	for i in $cards.get_children():
		for n in i.get_children():
			i.remove_child(n)
			n.queue_free()
	var i = 0
	phase = new_state["phase"]
	for hand in new_state['hands']:
		var j = 0
		for card in hand:
			var card_obj = $card.duplicate()
			var text: String = card
			card = text.substr(0, len(text) - 1)
			if text.ends_with("g"):
				card_obj.get_child(0).modulate = Color.GOLD
			elif text.ends_with("s"):
				card_obj.get_child(0).modulate = Color.SILVER
			elif text.ends_with("c"):
				card_obj.get_child(0).modulate = Color.CORAL
			elif text.ends_with("b"):
				card_obj.get_child(0).modulate = Color.BLACK
			else:
				card = text
			card_obj.get_child(0).text = card
			card_obj.position.x = j * 50
			card_obj.position.y = 0
			card_obj.connect("pressed", _click_card.bind(card))
			$cards.get_child(i).add_child(card_obj)
			j += 1
		i += 1

func _click_card(val):
	if (phase == 0):
		Utils.post(self, "playground/play_move", get_parent().request_completed, [], {"move": val, "game": "HighLow"})
	else:
		print("no")
	pass
