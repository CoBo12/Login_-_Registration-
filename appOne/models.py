from django.db import models
import re

class UserManager(models.Manager):
	def reg_validator(self,postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(postData['first_name']) < 3:
			errors['first_name'] = "First Name must be at least 3 characters."
		if len(postData['last_name']) < 3:
			errors['last_name'] = "Last Name must be at least 3 characters."
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Invalid Email'
		if len(postData['password']) < 8:
			errors['password'] = "Password must be at least 8 characters."
		if postData['password'] != postData['password_confirm']:
			errors['password_confirm'] = "Passwords do not match."
		return errors

	def login_validator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if not EMAIL_REGEX.match(postData['login_email']):
			errors['email'] = "Invalid Email/Password."
		if len(postData['login_password']) < 8:
			errors['login'] = "Invalid Email/Password"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_At = models.DateTimeField(auto_now=True)
	objects = UserManager()
