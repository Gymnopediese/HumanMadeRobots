extends Node

class_name Utils


static func post(sel, url, function = null, headers = [],  body = ""):
	var http_request = HTTPRequest.new()
	headers.push_back("Content-Type: application/json")

	if not url.begins_with("http"):
		url = "http://localhost:5000/" + url
	
	var cookies = Cookies.load()
	if cookies and "token" in cookies:
		headers.push_back("Authorization: Bearer " + cookies["token"])
		
	sel.add_child(http_request)
	if (function):
		http_request.request_completed.connect(function)
	body = JSON.new().stringify(body)
	print(body)
	var error = http_request.request(url, headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		push_error("An error occurred in the HTTP request.")

static func gett(sel, url: String, function, headers = []):
	
	if not url.begins_with("http"):
		url = "http://localhost:5000/" + url
	
	var http_request = HTTPRequest.new()
	sel.add_child(http_request)
	http_request.request_completed.connect(function)
	
	var cookies = Cookies.load()
	if cookies and "token" in cookies:
		headers.push_back("Authorization: Bearer " + cookies["token"])

	var error = http_request.request(url, headers)
	if error != OK:
		push_error("An error occurred in the HTTP request.")


static func request_completed(result, response_code, headers, body):
	var res = JSON.parse_string(body.get_string_from_utf8())
	print(body.get_string_from_utf8())
