from unittest import TestCase
from app import app
from flask import json


class ApiAuthTestCase(TestCase):
	"""
	this class tests the api
	"""

	def setUp(self):
		app.testing = True
		self.app = app.test_client()

	def tearDown(self):
		app.testing = False

	def test_register_user_success(self):
		payload = {
			"username": 'tester',
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		assert b"Tester's account has been created" in res.data

	def test_register_not_json(self):
		payload = {}

		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)

	def test_register_username_empty(self):
		payload = {
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)

	def test_register_password_empty(self):
		payload = {
			"username": 'tester',
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)

	def test_register_username_cannot_be_empty(self):
		payload = {
			"username": "  ",
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)
		assert b"username field cannot be empty" in res.data

	def test_register_password_must_be_8(self):
		payload = {
			"username": "tester",
			"password": "1234"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)
		assert b"password must be 8 characters or more" in res.data

	def test_register_username_exists(self):
		payload = {
			"username": "admin2",
			"password": "1234456789"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)
		assert b"username already exists. Please use a different username" in res.data
