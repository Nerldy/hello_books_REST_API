from flask import Flask, jsonify, abort, make_response, request
import uuid
import datetime as dt
import re

app = Flask(__name__)
app.url_map.strict_slashes = False


# useful functions
def format_inputs(word):
	"""
	formats input string
	:param word:
	:return: string
	"""
	json_input = word.title().strip()
	split_input = re.sub(' +', " ", json_input)
	return "".join(split_input)


books_collection = [
	{
		'id': '1',
		'title': 'Hello Books',
		'isbn': '456-569-968-1-123',
		'author': ['John Doe', "Janey Mishy"],
		'synopsis': "In place of a database we will store our task list in a memory structure. This will only work when the web server that runs our application is single process and single threaded. This is okay for Flask's own development web server. It is not okay to use this technique on a production web server, for that a proper database setup must be used."
	},
	{
		'id': "2",
		'title': 'Book 2',
		'isbn': '985-869-968-1-123',
		'author': ['John Doe', "Janey Mishy"],
		'synopsis': "In place of a database we will store our task list in a memory structure. This will only work when the web server that runs our application is single process and single threaded. This is okay for Flask's own development web server. It is not okay to use this technique on a production web server, for that a proper database setup must be used."
	}
]

user_registration_collection = [
	{
		'id': '1',
		'username': 'Admin1',
		'password': "admin1"
	},
	{
		'id': '2',
		'username': 'Admin2',
		'password': "admin2"
	},

]

user_logged_collection = []

allowed_keys = ['title', 'isbn', 'author', 'synopsis']  # needed book keys

borrowed_book_collection = []


@app.errorhandler(400)
def error_400(e):
	return make_response(jsonify({'error': 'Bad request'})), 400


@app.errorhandler(404)
def api_404_error_handler(error):
	return make_response(jsonify({"error": "Not found"})), 404


@app.errorhandler(401)
def api_401_error(e):
	return make_response(jsonify({'error': 'Unauthorized'})), 401


@app.route('/api/v1/books')
def api_get_all_books():
	return jsonify({'all books': books_collection})


@app.route('/api/v1/books/<string:book_id>')
def api_get_single_book(book_id):
	if book_id.isalnum() is False:
		return jsonify({"error": "make sure you're using web safe characters"}), 400
	single_book = [book for book in books_collection if book['id'] == book_id]

	if len(single_book) < 1:
		abort(404)
	return jsonify({"book": single_book[0]})


@app.route('/api/v1/books/', methods=['POST'])
def api_create_book():
	req_data = request.get_json()

	# Validate JSON data
	if not req_data:
		return jsonify({"error": "json object not detected"}), 400

	if 'title' not in req_data:
		return jsonify({"error": "'title' key not detected"}), 400

	if 'isbn' not in req_data:
		return jsonify({"error": "'isbn' key not detected"}), 400

	if 'author' not in req_data:
		return jsonify({"error": "'author' key not detected"}), 400

	if 'synopsis' not in req_data:
		return jsonify({"error": "'synopsis' key not detected"}), 400

	# validate ISBN
	isbn_data = req_data['isbn'].strip()
	if len(isbn_data) < 1:
		return jsonify({'error': "ISBN field cannot be empty"}), 400

	isbn_data_split = isbn_data.split("-")
	isbn_join = "".join(isbn_data_split)

	if isbn_join.isdigit() is not True:
		return jsonify({"error": "ISBN no, excluding the -, should only be in digits"}), 400

	if (len(isbn_join) != 10) and (len(isbn_join) != 13):
		return jsonify(
			{"error": "make sure the digits part of the ISBN(without the -), are either 10 digits or 13 digits"}), 400

	req_data_key_list = req_data.keys()

	if len(allowed_keys) < len(req_data_key_list):  # filter unrecognized keys
		for key in req_data:
			if key not in allowed_keys:
				return jsonify({"error": f"{key} is an unrecognized key"}), 400

	for bookISBN in books_collection:  # confirm ISBN doesn't exist
		if bookISBN['isbn'] == req_data['isbn']:
			return jsonify({'error': f"ISBN no. {req_data['isbn']} already exists. ISBN number MUST be unique"}), 400

	if isinstance(req_data['author'], list) is False:
		return jsonify({'error': 'author must be of list type'}), 400

	# validate author
	new_author = []
	for author in req_data['author']:
		if len(author.strip()) < 1:
			return jsonify({'error': 'author list cannot contain an empty field'}), 400
		else:
			new_author.append(format_inputs(author))

	req_data['author'] = new_author

	# validate synopsis
	if len(req_data['synopsis']) < 50:
		return jsonify({"error": "synopsis must be at least 50 characters long"}), 400

	single_book = {  # Book blueprint
		'id': uuid.uuid4().hex,
		'title': format_inputs(req_data['title']),
		'isbn': req_data['isbn'],
		'author': req_data['author'],
		'synopsis': req_data['synopsis'],
		"date_created": dt.datetime.now()
	}

	books_collection.append(single_book)  # add to book collection
	return jsonify({'Book successfully created': single_book}), 201


@app.route('/api/v1/books/<string:book_id>', methods=['PUT'])
def api_update_book(book_id):
	"""
	updates book
	:param book_id:
	:return:
	"""
	if book_id.isalnum() is False:
		return jsonify({"error": "make sure you're using web safe characters"}), 400

	update_book = [book for book in books_collection if book['id'] == book_id]

	req_data = request.get_json()
	if not request.json:
		abort(400)

	if 'title' in request.json:
		title = format_inputs(req_data['title'])

		if len(title) < 1:
			abort(400)
		else:
			request.json['title'] = title

	if 'author' in request.json:
		if isinstance(req_data['author'], list) is False:
			abort(400)

		# validate author
		new_author = []
		for author in request.json['author']:
			if len(author.strip()) < 1:
				return jsonify({'error': 'author list cannot contain an empty field'}), 400
			else:
				new_author.append(format_inputs(author))

		request.json['author'] = new_author

	if 'synopsis' in request.json:
		# validate synopsis
		if len(request.json['synopsis']) < 50:
			abort(400)

	update_book[0]['title'] = request.json.get('title', update_book[0]['title'])
	update_book[0]['author'] = request.json.get('author', update_book[0]['author'])
	update_book[0]['synopsis'] = request.json.get('synopsis', update_book[0]['synopsis'])
	return jsonify({"Book updated": update_book[0]})


@app.route('/api/v1/books/<string:book_id>', methods=['DELETE'])
def api_delete_book(book_id):
	"""
	delete book function
	:param book_id:
	:return:
	"""
	if book_id.isalnum() is False:
		return jsonify({"error": "make sure you're using web safe characters"}), 400

	delete_book = [book for book in books_collection if book['id'] == book_id]

	if len(delete_book) < 1:
		abort(404)

	books_collection.remove(delete_book[0])
	return jsonify({"result": True})


@app.route('/api/v1/users/books/<string:book_id>', methods=['POST'])
def api_borrow_book(book_id):
	"""
	function for user borrow book
	:param book_id:
	:return: 200, 404
	"""

	if book_id.isalnum() is False:
		return jsonify({"error": "make sure you're using web safe characters"}), 400

	borrowed_book = [book for book in books_collection if book['id'] == book_id]

	if len(borrowed_book) < 1:
		abort(404)

	borrowed_book_collection.append(borrowed_book[0])

	return jsonify({"borrowed book": borrowed_book[0]})


@app.route('/api/v1/auth/register', methods=['POST'])
def api_register():
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		abort(401)
	if 'password' not in request.json:
		abort(401)

	if 'username' in request.json:
		username = format_inputs(request.json['username'])

		if len(username) < 1:
			return jsonify({"error": "username field cannot be empty"}), 401
		else:
			request.json['username'] = username

	if 'password' in request.json:
		request.json['password'] = request.json['password'].strip()
		split_password = request.json['password'].split(" ")
		join_password = "".join(split_password)

		if len(join_password) != len(request.json['password']):
			return jsonify({"error": "password cannot have space characters in it"}), 401

		if len(request.json['password']) < 8 or request.json['password'] == "":
			return jsonify({"error": "password must be 8 characters or more"}), 401

	new_user = [user for user in user_registration_collection if user['username'] == request.json['username']]

	if len(new_user) == 0:
		create_user = {
			'id': uuid.uuid4().hex,
			'username': request.json['username'],
			'password': request.json['password'],
			'date_created': dt.datetime.now()
		}
		user_registration_collection.append(create_user)
		return jsonify({"message": f"{request.json['username']}'s account has been created"}), 201

	return jsonify({"error": "username already exists. Please use a different username"}), 401


@app.route('/api/v1/auth/login', methods=['POST'])
def api_login():
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		abort(401)
	if 'password' not in request.json:
		abort(401)

	request.json['username'] = format_inputs(request.json['username'])

	# check if user is registered
	is_user_reg = [user for user in user_registration_collection if user['username'] == request.json['username']]

	# check if user is logged in
	is_user_logged = [user for user in user_logged_collection if user['username'] == request.json['username']]

	if len(is_user_reg) < 1:
		return jsonify({'error': "user not found. Please register first"}), 401

	if is_user_logged:
		return jsonify({"message": "you're already logged in"})

	# log in user
	if (is_user_reg[0]['username'] == request.json['username']) and (
			is_user_reg[0]['password'] == request.json['password']):
		user_logged_collection.append(is_user_reg[0])
		return jsonify({"success": f"logged in as {request.json['username']} "})

	return jsonify({'error': "username or password don't match"}), 401


@app.route('/api/v1/auth/logout', methods=['POST'])
def api_logout():
	if not request.json:
		abort(404)

	user_logged_out = user_logged_collection.pop()

	return jsonify({"message": f"logged out {user_logged_out['username']}"})


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def api_reset_password():
	if not request.json:
		return jsonify({"error": "json not detected"}), 401

	if 'username' not in request.json:
		return jsonify({"error": "username key not detected in json"}), 401

	if 'old_password' not in request.json:
		return jsonify({"error": "old_password key not detected in json"}), 401

	if 'new_password' not in request.json:
		return jsonify({"error": "new_password key not detected in json"}), 401

	if 'username' in request.json:
		username = format_inputs(request.json['username'])

		if len(username) < 1:
			return jsonify({"error": "username field cannot be empty"}), 401
		else:
			request.json['username'] = username

	if 'new_password' in request.json:
		request.json['new_password'] = request.json['new_password'].strip()
		split_password = request.json['new_password'].split(" ")
		join_password = "".join(split_password)

		if len(join_password) != len(request.json['new_password']):
			return jsonify({"error": "password cannot have space characters in it"}), 401

		if len(request.json['new_password']) < 8 or request.json['new_password'] == "":
			return jsonify({"error": "password must be 8 characters or more"}), 401

	# check if username exists in registrations
	find_user = [user for user in user_registration_collection if user['username'] == request.json['username']]

	# if user doesn't exist ask them to register
	if len(find_user) < 1:
		return jsonify({"message": "username not found. Please register"}), 404

	# if they do, check if if old password match the one in the database
	if find_user[0]['password'] == request.json['old_password']:
		find_user[0]['password'] = request.json['new_password']
		return jsonify({"message": "password updated successfully"})

	abort(401)


# if they do, update password with the new one
# else tell them passwords don't match

if __name__ == '__main__':
	app.run(debug=1)
