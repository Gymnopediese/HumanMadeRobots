class_name Cookies extends Node



const FILE_NAME = "user://game-data.json"

static func save(token):
	var file = FileAccess.open(FILE_NAME, FileAccess.WRITE)
	file.store_line(JSON.stringify(token))
	file.close()

static func load():
	var data = null
	if FileAccess.file_exists(FILE_NAME):
		var file = FileAccess.open(FILE_NAME, FileAccess.READ)
		data = JSON.parse_string(file.get_as_text())
		file.close()
	else:
		printerr("No saved data!")
	return data
