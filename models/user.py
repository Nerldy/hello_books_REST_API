from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import datetime as dt


class CreateUser:

	def __init__(self):
		self.id = uuid.uuid4().hex
		self.username = None
		self.password = None
		self.date_created = dt.datetime.now()

	def set_username(self, username):
		self.username = username

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def get_id(self):
		return self.id

	def get_username(self):
		return self.username

	def get_password(self):
		return self.password

	def get_date_created(self):
		return self.date_created



