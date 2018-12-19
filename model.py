"""Models and database functions for RoboRemindMe"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##### Model definitions #####

class User(db.Model):
	"""Roboreminder registered users"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autocrement=True, primary_key=True)
	username = db.Column(db.String(25), nullable=False)
	phone_num = db.Column(db.String(50)) #needs to verify in order to gain full access
	password = db.Column(db.String(200), nullable=False)

	#Define relationship to messages
	messages = db.relationship("")

	def __repr__(self):
		"""Provide clear representation when printed"""

class SmsMessages(db.Model):
	"""Storage of messages and it's details"""

	__tablename__ = "messages"

	message_id = db.Column(db.Integer, autocrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	recipent = db.Column(db.String(50))
	