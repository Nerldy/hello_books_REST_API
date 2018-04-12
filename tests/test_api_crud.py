from unittest import TestCase
from app import app
from flask import json


class ApiTestCRUDCases(TestCase):
	"""
	this class tests the api
	"""

	def setUp(self):
		app.testing = True
		self.app = app.test_client()

	def tearDown(self):
		app.testing = False

	def test_get_all_books(self):
		res = self.app.get('/api/v1/books')
		assert b"all books" in res.data

	def test_get_book_id_web_safe(self):
		res = self.app.get("/api/v1/books/69++")
		self.assertEqual(res.status_code, 400)

	def test_get_book_with_id_successful(self):
		res = self.app.get("/api/v1/books/1")
		self.assertEqual(res.status_code, 200)
		assert b"book" in res.data

	def test_get_book_with_id_error(self):
		res = self.app.get("/api/v1/books/19")
		self.assertEqual(res.status_code, 404)

	def test_create_book(self):
		payload = {
			"title": "Create Book",
			"isbn": "4567894123",
			"author": ["John Doe"],
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"Book successfully created" in res.data
		self.assertEqual(res.status_code, 201)

	def test_create_book_isbn_not_10_or_13(self):
		payload = {
			"title": "Create Book",
			"isbn": " 123-984-9852-32              ",
			"author": "John Doe",
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b" are either 10 digits or 13 digits" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_empty_isbn_error(self):
		payload = {
			"title": "Create Book",
			"isbn": "              ",
			"author": "John Doe",
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"ISBN field cannot be empty" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_isbn_is_numbers(self):
		payload = {
			"title": "Create Book",
			"isbn": "      569-985u96        ",
			"author": "John Doe",
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"ISBN no, excluding the -, should only be in digits" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_author_cannot_be_empty(self):
		payload = {
			"title": "Create Book",
			"isbn": "      12345-987-96        ",
			"author": ["   ", "Tidy"],
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"author list cannot contain an empty field" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_synopsis_not_less_than_50(self):
		payload = {
			"title": "Create Book",
			"isbn": "      12345-987-96        ",
			"author": ["Tidy"],
			"synopsis": "The delete_task"
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"synopsis must be at least 50 characters long" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_unrecognized_key_error(self):
		payload = {
			"title": "Create Book",
			"isbn": "4567894123",
			"author": ["John Doe"],
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database.",
			"foo": ""
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"foo is an unrecognized key" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_isbn_number_unique(self):
		payload = {
			"title": "Create Book",
			"isbn": "456-569-968-1-123",
			"author": ["John Doe"],
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"ISBN number MUST be unique" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_author_must_be_list_type(self):
		payload = {
			"title": "Create Book",
			"isbn": "1234571101236",
			"author": "John Doe",
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"author must be of list type" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_empty_json_not_detected(self):
		payload = {}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"json object not detected" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_title_key_not_detected(self):
		payload = {
			"isbn": "569-698-587-5",
			"author": ["5", "pola  ", "dummba"],
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"'title' key not detected" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_no_author_error(self):
		payload = {
			"title": "Create Book",
			"isbn": "4567894123",
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"'author' key not detected" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_no_synopsis_error(self):
		payload = {
			"title": "Create Book",
			"isbn": "4567894123",
			"author": ["John Doe"]
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"'synopsis' key not detected" in res.data
		self.assertEqual(res.status_code, 400)

	def test_create_book_no_isbn_error(self):
		payload = {
			"title": "Create Book",
			"author": ["John Doe"],
			"synopsis": "The delete_task function should have no surprises. For the update_task function we are trying to prevent bugs by doing exhaustive checking of the input arguments. We need to make sure that anything that the client provided us is in the expected format before we incorporate it into our database."
		}
		res = self.app.post('/api/v1/books', data=json.dumps(payload), content_type='application/json')
		assert b"'isbn' key not detected" in res.data
		self.assertEqual(res.status_code, 400)

	def test_remove_book_web_safe(self):
		res = self.app.delete('/api/v1/books/+69+')
		assert b"web safe" in res.data

	def test_remove_book_404_error(self):
		res = self.app.delete('/api/v1/books/568')
		self.assertEqual(res.status_code, 404)

	def test_remove_book_successful(self):
		res = self.app.delete('/api/v1/books/1')
		self.assertEqual(res.status_code, 200)

	def test_update_book_succesful(self):
		payload = {
			"title": "New Book",
			"author": ["new author"],
			"synposis": "The server has fulfilled the request but does not need to return an entity-body, and might want to return updated metainformation. The response MAY include new or updated metainformation in the form of entity-headers, which if present SHOULD be associated with the requested variant."
		}

		res = self.app.put('/api/v1/books/2', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 200)
		assert b"updated" in res.data

	def test_update_web_safe_error(self):
		res = self.app.put('api/v1/books/2+69*')
		assert b"web safe" in res.data

	def test_update_not_json(self):
		res = self.app.put('api/v1/books/1', data=[])
		self.assertEqual(res.status_code, 400)

	def test_update_empty_title_error(self):
		payload = {
			"title": "  ",
		}
		res = self.app.put('/api/v1/books/2', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 400)
		assert b"Bad request" in res.data

	def test_update_author_not_list_aborts(self):
		payload = {
			"author": "  ",
		}
		res = self.app.put('/api/v1/books/2', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 400)
		assert b"Bad request" in res.data

	def test_update_author_not_empty(self):
		payload = {
			"author": ["  "],
		}
		res = self.app.put('/api/v1/books/2', data=json.dumps(payload), content_type='application/json')
		assert b"author list cannot contain an empty field" in res.data

	def test_update_synopsis_less_than_50_error(self):
		payload = {
			"synopsis": ""
		}
		res = self.app.put('/api/v1/books/2', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 400)

	def test_borrow_book_successful(self):
		res = self.app.post("/api/v1/users/books/2")
		self.assertEqual(res.status_code, 200)

	def test_borrow_book_web_safe(self):
		res = self.app.post("/api/v1/users/books/2++")
		self.assertEqual(res.status_code, 400)

	def test_borrow_book_no_book_found(self):
		res = self.app.post("/api/v1/users/books/100")
		self.assertEqual(res.status_code, 404)
