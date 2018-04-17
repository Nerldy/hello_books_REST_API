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
			"username": 'paul',
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		assert b"paul's account has been created" in res.data

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

	def test_register_password_cannot_have_space(self):
		payload = {
			"username": "tester",
			"password": "1234  4567896"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)
		assert b"password cannot have space characters" in res.data

	def test_register_username_exists(self):
		payload = {
			"username": "admin2",
			"password": "1234456789"
		}
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		res = self.app.post('/api/v1/auth/register', data=json.dumps(payload), content_type='application/json')
		self.assertEqual(res.status_code, 401)
		assert b"username already exists. Please use a different username" in res.data

	def test_login_success(self):
		payload = {
			"username": "tester",
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		assert b"logged in as tester" in res.data

	def test_login_already_logged_in(self):
		payload = {
			"username": "tester",
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		res2 = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		assert b"You're already logged in" in res2.data

	def test_login_log_out_first(self):
		payload = {
			"username": "tester",
			"password": "123456789"
		}
		payload2 = {
			"username": "tester2",
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		res2 = self.app.post('/api/v1/auth/register', data=json.dumps(payload2), content_type='application/json')
		res3 = self.app.post('/api/v1/auth/login', data=json.dumps(payload2), content_type='application/json')
		assert b"you must log out first" in res3.data

	def test_login_no_json(self):
		payload = ""
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		assert res.status_code == 401

	def test_login_no_username_error(self):
		payload = {
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		assert res.status_code == 401

	def test_login_no_password_error(self):
		payload = {
			"username": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		assert res.status_code == 401

	def test_login_user_not_exist(self):
		payload = {
			"username": "the_sun",
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		assert b"username doesn't exists" in res.data

	def test_logout(self):
		payload = {
			"username": "tester",
			"password": "123456789"
		}
		res = self.app.post('/api/v1/auth/login', data=json.dumps(payload), content_type='application/json')
		res = self.app.post('/api/v1/auth/logout', data=json.dumps(dict(username='tester')),
							content_type='application/json')
		assert b"successfully logged out" in res.data

	def test_logout_no_json(self):
		payload = ""
		res = self.app.post('/api/v1/auth/logout', data=json.dumps(payload), content_type='application/json')
		assert res.status_code == 401

	def test_logout_no_username(self):
		payload = {"nothing": "u"}
		res = self.app.post('/api/v1/auth/logout', data=json.dumps(payload), content_type='application/json')
		assert b"username required to log out" in res.data
		assert res.status_code == 401

	def test_logout_already_logged_out(self):
		payload = {
			"username": "tester"
		}
		res = self.app.post('/api/v1/auth/logout', data=json.dumps(payload), content_type='application/json')
		res = self.app.post('/api/v1/auth/logout', data=json.dumps(payload), content_type='application/json')
		assert res.status_code == 401

	def test_reset_password_succesful(self):
		payload = {
			"username": 'tester',
			"old_password": "123456789",
			"new_password": "987654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"password has been reset" in res.data

	def test_reset_password_no_json_error(self):
		payload = ""

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert res.status_code == 401

	def test_reset_password_no_username_error(self):
		payload = {
			"old_password": "123456789",
			"new_password": "987654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"username field not found" in res.data

	def test_reset_password_no_old_pw_error(self):
		payload = {
			"username": 'tester',
			"new_password": "987654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"old_password field not found" in res.data

	def test_reset_pw_no_new_pw_error(self):
		payload = {
			"username": 'tester',
			"old_password": "987654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"new_password field not found" in res.data

	def test_reset_pw_user_not_found(self):
		payload = {
			"username": 'tester3',
			"old_password": "123456789",
			"new_password": "987654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"user not found" in res.data

	def test_reset_pw_new_pw_cant_have_space(self):
		payload = {
			"username": 'tester',
			"old_password": "123456789",
			"new_password": "98 7654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"new_password cannot have space characters in it" in res.data

	def test_reset_pw_new_pw_must_be_8_characters(self):
		payload = {
			"username": 'tester',
			"old_password": "123456789",
			"new_password": "654321"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"new_password must be 8 characters or more" in res.data

	def test_reset_pw_username_or_password_not_correct(self):
		payload = {
			"username": 'tester',
			"old_password": "12345678",
			"new_password": "654321896565"
		}

		res = self.app.post('/api/v1/auth/reset-password', data=json.dumps(payload), content_type='application/json')
		assert b"username or old_password is not correct" in res.data
