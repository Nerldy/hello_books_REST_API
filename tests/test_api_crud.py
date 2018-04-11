from unittest import TestCase
from app import app

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