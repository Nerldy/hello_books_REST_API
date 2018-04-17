from flask import Flask, jsonify, abort, make_response, request
from models.user import CreateUser
import uuid
import datetime as dt
import re
from werkzeug.security import check_password_hash, generate_password_hash

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

user_tester = CreateUser()
user_tester.set_username('tester')
user_tester.set_password('123456789')

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
	{
		'id': user_tester.get_id(),
		"username": user_tester.get_username(),
		"password": user_tester.get_password()
	}

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
			request.json['username'] = username.lower()

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
		user_blueprint = CreateUser()
		user_blueprint.set_username(request.json['username'])
		user_blueprint.set_password(request.json['password'])

		create_user = {
			'id': user_blueprint.get_id(),
			'username': user_blueprint.get_username(),
			'password': user_blueprint.get_password(),
			'date_created': user_blueprint.get_date_created()
		}

		user_registration_collection.append(create_user)
		return jsonify({"message": f"{request.json['username']}'s account has been created"}), 201

	return jsonify({"error": "username already exists. Please use a different username"}), 401


@app.route('/api/v1/auth/login', methods=['POST'])
def api_login():
	# confirm json is in the request object
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		abort(401)

	if 'password' not in request.json:
		abort(401)

	# check if username already exists in the registered list
	check_user = [user for user in user_registration_collection if user['username'] == request.json['username']]

	# if not ask user to register
	if len(check_user) < 1:
		return jsonify({"error": "username doesn't exists. Please register first"}), 401

	# check if user is already logged in
	for user in user_logged_collection:
		if user['username'] == check_user[0]['username']:
			return jsonify({"message": f"You're already logged in as {request.json['username']}"})
		else:
			# then user must first logout to login with a new username
			return jsonify(
				{"error": f"you must log out first from {user_logged_collection[0]['username']}'s account"})

	# if they exist check if password match
	if check_password_hash(check_user[0]['password'], request.json['password']):
		# add user to logged in list
		user_logged_collection.append(check_user[0])
		return jsonify({"success": f"logged in as {request.json['username']}"})

	# if not send back error message that password or username don't match'
	return jsonify({'error': "username or password don't match. Please try again."}), 401


@app.route('/api/v1/auth/logout', methods=['POST'])
def api_logout():
	global user_logged_collection
	# confirm json is in the request object
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		return jsonify({"error": "username required to log out"}), 401

	for user in user_logged_collection:
		if user['username'] == request.json['username']:
			# check if user is logged in
			user_logged_collection = list(filter(lambda x: x['username'] != request.json['username'], user_logged_collection))

			return jsonify({"message": f"{request.json['username']} successfully logged out"})

	return jsonify({"error": f"can't logout {request.json['username']} because it's not currently logged in"}), 401


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def api_reset_password():
	if not request.json:
		abort(401)

	if 'username' not in request.json:
		return jsonify({"error": "username field not found in json"}), 401

	if 'old_password' not in request.json:
		return jsonify({"error": "old_password field not found in json"}), 401

	if 'new_password' not in request.json:
		return jsonify({"error": "new_password field not found in json"}), 401

	# search if user is registered
	is_user_registered = next(filter(lambda x: x['username'] == request.json['username'], user_registration_collection), None)

	if is_user_registered is None:
		return jsonify({"message": "user not found. Please register"}), 404
	else:
		if 'new_password' in request.json:
			request.json['new_password'] = request.json['new_password'].strip()
			split_password = request.json['new_password'].split(" ")
			join_password = "".join(split_password)

			if len(join_password) != len(request.json['new_password']):
				return jsonify({"error": "new_password cannot have space characters in it"}), 401

			if len(request.json['new_password']) < 8 or request.json['new_password'] == "":
				return jsonify({"error": "new_password must be 8 characters or more"}), 401

		# check if old password match
		if check_password_hash(is_user_registered['password'], request.json['old_password']):
			update_password = {
				"password": generate_password_hash(request.json["new_password"])
			}
			is_user_registered.update(update_password)

			return jsonify({"message": "password has been reset"})

		return jsonify({'error': "username or old_password is not correct"}), 401


if __name__ == '__main__':
	app.run(debug=1)
