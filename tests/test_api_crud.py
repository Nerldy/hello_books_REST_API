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



