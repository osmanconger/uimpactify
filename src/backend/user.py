import mongoengine as me
import hashlib
from flask import Flask, make_response, request, jsonify
from Exceptions.MissingRequiredField import checkFields


class UserObj():
	"""
	This class holds all the CRUD methods for the users
	"""
	
	# generic user class inheriting the mongo document 
	class User(me.Document):

		user_type = me.StringField()
		username = me.StringField()
		password = me.StringField()
		email = me.StringField()

		def to_json(self):
			"""
			Returns the user object as a json.
			"""

			return {
				"user_type": self.user_type,
				"username": self.username,
				"password": self.password, 
				"email": self.email
			}

	def __init__(self, content):
		"""
		Instantiates a new instance of UserObj
		"""

		self.content = content
		self.hash_password()
	
	def hash_password(self):
		"""
		Hashes the password. The database does not need to know what the password is.
		"""
		if 'password' in self.content:
			self.content['password'] = hashlib.sha224(self.content['password'].encode()).hexdigest()

	def db_create_user(self):
		"""
		Saves the current user to the database.
		"""

		x = checkFields(self.content, fields=['user_type', 'username', 'password', 'email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		if (self.User.objects(username=self.content['username']).count() > 0):
			return make_response("Username already in use.", 400)
		if (self.User.objects(email=self.content['email']).count() > 0):
			return make_response("Email already in use.", 400)

		self.User(user_type=self.content['user_type'], username=self.content['username'], password=self.content['password'], email=self.content['email']).save()
		return make_response("", 200)
	
	def db_get_user(self):
		"""
		Creates the user based off of the email passed in.
		"""

		x = checkFields(self.content, fields=['email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		user_obj = self.User.objects(email=self.content['email']).first()
		if user_obj:
			return make_response(jsonify(user_obj.to_json()), 200)
		else:
			return make_response("", 404)

	def db_update_user_name(self):
		"""
		Updates the username in the database for the corresponding email
		"""

		x = checkFields(self.content, fields=['username', 'email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		user_obj = self.User.objects(email=self.content['email']).first()
		if user_obj:
			user_obj.update(username=self.content['username'])
			return make_response("", 200)
		else:
			return make_response("User does not exist.", 404)
	
	def db_update_user_password(self):
		"""
		Updates the password in the database for the corresponding email
		"""

		x = checkFields(self.content, fields=['password', 'email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		user_obj = self.User.objects(email=self.content['email']).first()
		if user_obj:
			user_obj.update(password=self.content['password'])
			return make_response("", 200)
		else:
			return make_response("User does not exist.", 404)

	def db_update_user_email(self):
		"""
		Updates the email in the database for the corresponding email
		"""

		x = checkFields(self.content, fields=['old_email', 'new_email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		user_obj = self.User.objects(email=self.content['old_email']).first()
		if user_obj:
			user_obj.update(email=self.content['new_email'])
			return make_response("", 200)
		else:
			return make_response("User does not exist.", 404)

	def db_delete_single_user(self):
		"""
		Delete a single user in the database
		"""

		x = checkFields(self.content, fields=['email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		user_obj = self.User.objects(email=self.content['email']).first()
		if user_obj:
			user_obj.delete()
			return make_response("", 200)
		else:
			return make_response("User does not exist.", 404)

	def db_delete_all_users(self):
		"""
		Deletes all user in the database
		"""

		for user in self.User.objects():
			user.delete()
		return make_response("", 200)

	def db_login(self):
		"""
		Logs in using the username and password given
		"""

		x = checkFields(self.content, fields=['password', 'email'])
		if (x):
			return make_response("Missing required field: " + x, 400)

		user_obj = self.User.objects(email=self.content['email'], password=self.content['password']).first()
		if user_obj:
			return make_response(jsonify("true"), 200)
		else:
			return make_response(jsonify("false"), 200)