"""Models and database functions for RoboRemindMe"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##### Model definitions #####

class User(db.Model):
	"""Roboreminder registered users"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	username = db.Column(db.String(25), nullable=False)
	phone_num = db.Column(db.String(50)) # Needs to verify in order to gain full access
	password = db.Column(db.String(200), nullable=False)

	# Define relationship to reminders
	reminders = db.relationship("")

	def __repr__(self):
		"""Provide clear representation when printed"""

		return "<User user_id={} username={} phone_num={} password={}>".format(
																		self.user_id,
																		self.username,
																		self.phone_num,
																		self.password)

class Reminder(db.Model):
	"""Storage of reminders and it's details"""

	__tablename__ = "reminders"

	message_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	recipent = db.Column(db.String(50), nullable=False)
	date_created = db.Column(db.String(50), nullable=False) # Current date/time of message created
	date_sent = db.Column(db.String(50), nullable=False) # date/time of when to send message or when message was sent
	body = db.Column(db.String(55), nullable=False) 
	sid = db.Column(db.String(200))
	status = db.Column(db.String(10))

	def __repre__(self):
		"""Provide clear representation when printed"""

		return "<Reminder message_id={} user_id={} recipent={} date_created={} date_sent={} body={} sid={}>".format(
																												self.message_id,
																												self.user_id,
																												self.recipent,
																												self.date_created,
																												self.date_sent,
																												self.body,
																												self.sid)





##### Helper Functions #####

def connect_to_db(app):
	"""Connect the database to our Flask app"""

	# Configure to use our PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reminders'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	# If we run this module interactively, it will leave you in 
	# a state of being able to work with the database directly.

	from robo import app
	connect_to_db(app)
	print("Connected to DB") 