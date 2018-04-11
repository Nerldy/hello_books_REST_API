from flask import Flask, jsonify, abort, make_response, request
import uuid
import datetime as dt
import re

app = Flask(__name__)
app.url_map.strict_slashes = False


# useful functions
def format_book_input_values(word):
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

allowed_keys = ['title', 'isbn', 'author', 'synopsis']  # needed book keys


@app.errorhandler(400)
def error_400(e):
	return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def api_404_error_handler(error):
	return make_response(jsonify({"error": "Not found"})), 404


@app.route('/api/v1/books')
def api_get_all_books():
	return jsonify({'books': books_collection})


@app.route('/api/v1/books/<string:book_id>')
def api_get_single_book(book_id):
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

	# format author
	new_author = []
	for author in req_data['author']:
		if len(author.strip()) < 1:
			return jsonify({'error': 'author list cannot contain an empty field'}), 400
		else:
			new_author.append(format_book_input_values(author))

	req_data['author'] = new_author

	single_book = {  # Book blueprint
		'id': uuid.uuid4().hex,
		'title': format_book_input_values(req_data['title']),
		'isbn': req_data['isbn'],
		'author': req_data['author'],
		'synopsis': req_data['synopsis'],
		"date_created": dt.datetime.now()
	}

	books_collection.append(single_book)  # add to book collection
	return jsonify({'Book successfully created': single_book})


if __name__ == '__main__':
	app.run(debug=1)
