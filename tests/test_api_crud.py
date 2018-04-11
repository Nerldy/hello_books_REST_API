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
