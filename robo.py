from flask import Flask, request, render_template, flash, redirect, session, url_for
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from authy.api import AuthyApiClient
from datetime import datetime, timedelta
from config2 import *
from werkzeug.security import generate_password_hash, check_password_hash
from model import connect_to_db, db, User, Reminder

app = Flask(__name__)
app.config.from_object('config')

api = AuthyApiClient(app.config['AUTHY_API_KEY'])
app.secret_key = app.config['SESSION_SKEY']
account_sid = app.config['ACCOUNT_NUM']
auth_token = app.config["TOKEN_NUM"]
client = Client(account_sid, auth_token)
connect_to_db(app)

########### Functions begin ##############

@app.route("/")
def index():
	"""Log in/ Register page."""
	return render_template("mainpage.html")

@app.route("/", methods=["POST"])
def login():
	""" Login"""
	username = request.form.get('username')
	username = username.lower()
	unhashed_pw = request.form.get('password')
	user_cred = User.query.filter_by(username=username).first()

	# If username doesn't exist inside the database
	if user_cred is None:
		flash("Username not found! try again or register")
		return render_template("mainpage.html")

	# Checks to see if password matches password inside the db
	if check_password_hash(user_cred.password, unhashed_pw):
		session['username'] = username
		if user_cred.phone_num is None:
			flash("Welcome back! You must verify your phone number to complete registration.")
			return render_template("phone_verification.html")
		# If registration is complete, user gets full access
		return render_template("homepage.html")
	else:
		flash("Incorrect password, try again!")
		return render_template("mainpage.html")	

@app.route("/logout")
def logout():
	"""Removes the user from the session and logs them out."""
	session.pop('username', None)
	return redirect('/')

@app.route("/register",  methods=["GET","POST"])
def registration():
	"""Add new user to database"""
	if request.form.get("pw1") != request.form.get("pw2"):
		flash("Passwords didn't match!")
		return render_template("mainpage.html")
	else:
		username = request.form.get("new_username")
		username = username.lower()
		telephone = request.form.get("telephone")
		unhashed_pw = request.form.get("pw1")

		# This generates a password hash
		hashed_pw = generate_password_hash(unhashed_pw, method="sha256")
		password = hashed_pw

		
		# This checks if username is already in the db, if it's not, it's added
		print(username)
		if User.query.filter_by(username=username).first() is None:
			new_user = User(username=username, password=password)
			db.session.add(new_user)
			db.session.commit()
			session["username"] = username
			flash("Last step! You must verify your phone number in order to complete registration.")
			return redirect("/phone_verification")
		else:
			flash("Oh no! Looks like the username '{}' is already taken, choose a different username".format(username))
			return render_template("mainpage.html")

######### Phone verification for 2F #########
@app.route("/phone_verification")
def show_phone_verification():
	"""Display verification form."""
	return render_template("phone_verification.html")


@app.route("/phone_verification", methods=["POST"])
def phone_verification():
	"""Grabs input from the form."""
	country_code = request.form.get("country_code")
	phone_number = request.form.get("phone_number")
	method = request.form.get("method")

	# Saves country_code and phone_number to the user's session
	# for when the user gets redirected to verify
	session['country_code'] = country_code
	session['phone_number'] = phone_number

	# Api call
	api.phones.verification_start(phone_number, country_code, via=method)

	return redirect(url_for("verify"))


@app.route("/verify")
def show_verification():
	"""Displays validation form."""
	return render_template("verify.html")	


@app.route("/verify", methods=["POST"])
def verify():
	"""validates user's input."""
	token = request.form.get("token")

	# Grabs the user's creds from the session
	phone_number = session['phone_number']
	country_code = session['country_code']

	verification = api.phones.verification_check(phone_number, country_code, token)

	if verification.ok():
		if 'username' in session:
			username = session['username']
			user = User.query.filter_by(username=username).first()
			user.phone_num = phone_number
			db.session.commit()
			flash("Welcome to Roboremind me!")
			return redirect("/sms")
		else:
			flash("Something went wrong! Please log in and verify again")
			return redirect("/")

	else:
		flash("Wrong verification code")
		return redirect(url_for("verify"))



@app.route("/sms")
def show_homepage():
	"""displays homepage"""
	if 'username' not in session:
		return redirect('/')

	# If user hasn't verified their phone number, redirect to verification page
	user_cred = User.query.filter_by(username=session['username']).first()
	if user_cred.phone_num is None:
		flash("You must verify your phone number to complete registration")
		return render_template("phone_verification.html")

	
	return render_template("homepage.html")

# Refactor - Work in Progress...
@app.route("/sms", methods=["POST"])
def homepage():
	"""Displays page to send reminder."""
	
	# recipent's phone number
	text_num = request.form.get("phone")
	
	# message sent to recipent
	msg = request.form.get("reminder")
	# send immediately option
	sendnow = request.form.get("textrn")
	# temp flag to print needed info
	timedate_info = False
	
	# if user doesn't check 'send immediately' option
	# i want to save the reminder in the database with 'pending' status until cron runs and executes to send
	if sendnow == None:
		time_date = True
		time = request.form.get("texttime")
		date = request.form.get("textdate")
		timezone = request.form.get("timezone")
		# seconds are added to time, for better formatting
		time = time + ':00'
		send_date = date + " " + time[0:8]
		# convert user's local time to utc
		send_date = convertlocal_utc(send_date, timezone)
		# Save the message in the db with the time/date(created), recipent num and status 'pending'
		# Send the message when that time/date matches current t/d, changing status to 'sent'
		# Then save the sid
		message = client.messages \
				.create(
					body = msg,
					from_= app.config["TWILIO_SMSNUM"],
					to = text_num,
					status_callback = "http://www.roboremindme.ngrok.io/sms_to_db",
					#Status= "sent"
					)
	else:
		send_date = datetime.now()
		message = client.messages \
				.create(
					body = msg,
					from_= app.config["TWILIO_SMSNUM"],
					to = text_num,
					status_callback = "http://www.roboremindme.ngrok.io/sms_to_db",
					#Status= "sent",
					#status_callback_method= "POST"
					)

	# save to, time created, time sent, message, sid insiide the database.
	if timedate_info == True:
		print("time = {}".format(time))
		print("date = {}".format(date))
		print("message sid = {}".format(message.sid))
		print("message recipent = {}".format(message.to))
		print("message created(now it's current date) = {}".format(datetime.now()))
		print("message sent date = {}".format(send_date))
		print("message body = {}".format(message.body))
	print("message sid = {}".format(message.sid))
	print("message recipent = {}".format(message.to))
	print("message created(now it's current date) = {}".format(datetime.now()))
	print("message sent date = {}".format(send_date))
	print("message body = {}".format(message.body))

	return redirect("/sms")

@app.route("/sms_to_db", methods=['POST'])
def reminders_to_db():
	"""Adds sms data to db, Twilio sends info here when text is initiated"""
	# Get specific data info from sms via request.form
	data = request.form
	print("data = {}".format(data))
	recipient = data["to"]
	# Have to change datetime format
	date_created = data["date_created"]
	date_sent = data["date_sent"] # Date when to send, if date is not right now, status = pending
	body = data["body"]
	sid = data["sid"]
	status = data["status"] # If date sent is now rn, status = pending

	user = User.query.filter_by(username=session['username']).all()
	userid = user[0].user_id
	if userid > 0:
		new_reminder = Reminder(user_id=userid, recipent=recipient, date_created=date_created,
								date_sent=date_sent, body=body, sid=sid, status=status)
		db.session.add(new_reminder)
		db.session.commit()
		print(new_reminder)


	return "ok"

@app.route("/resp", methods=['GET', 'POST'])
def sms_reply():
	"""Send a dynamic reply to an incoming text message."""
	# Get the message the user sent our app number
	body = request.values.get('Body', None)

	# Start our TwiML response
	resp = MessagingResponse()
	

	# Determine the right reply for this message
	body = body.lower()
	if body == "hello" or body == "hi":
		resp.message("Hi!")
	elif "your name" in body:
		resp.message("She named me Roboremindme, but you can call me Watson")
	elif "picture" in body:
		pic = resp.message("Here's my contact picture. Save it under Roboremindme!")
		pic.media("https://c1.staticflickr.com/5/4894/31633985757_1886a7bb04_b.jpg")
	else:
		resp.message("Roboremindme is here to remind you to get things done.")

	

	return str(resp)


if __name__ == "__main__":
	#pass
	app.run(debug=True, host="0.0.0.0")