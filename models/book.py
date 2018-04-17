import uuid
import datetime as dt


class Book:
	"""creates a book instance"""

	def __init__(self):
		self.id = uuid.uuid4().hex
		self.title = None
		self.isbn = None
		self.author = None
		self.synopsis = None
		self.date_created = dt.datetime.now()

	def set_title(self, title):
		self.title = title

	def set_isbn(self, isbn):
		self.isbn = isbn

	def set_author(self, author):
		self.author = author

	def set_synopsis(self, synopsis):
		self.synopsis = synopsis

	def get_id(self):
		return self.id

	def get_title(self):
		return self.title

	def get_isbn(self):
		return self.isbn

	def get_author(self):
		return self.author

	def get_synopsis(self):
		return self.synopsis

	def get_date_created(self):
		return self.date_created
