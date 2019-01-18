from flask import Flask, request, render_template, flash, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import datetime, timedelta
from config import *; from config2 import *

app = Flask(__name__)

account_sid = account_sid("account_num")
auth_token = auth_token("token_num")

client = Client(account_sid, auth_token)
# It's a great thing when you realize you still have the ability to surprise yourself. 

########### Functions begin ##############

@app.route("/sms")
def index():
	"""displays homepage"""
	return render_template("homepage.html")

# Refactor - Work in Progress...
@app.route("/sms", methods=["GET", "POST"])
def testing_homepage():
	
	# recipent's phone number
	text_num = request.form.get("phone")
	
	# message sent to recipent
	msg = request.form.get("reminder")
	# send immediately option
	sendnow = request.form.get("textrn")
	# temp flag to print needed info
	timedate_info = False
	
	# if user doesn't check 'send immediately' option
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
		# Save the message in the db with the time/date(created) and recipent num
		# Send the message when that time/date matches current t/d
		# Then save the sid
		message = client.messages \
				.create(
					body = msg,
					from_= twilio("twilio_num"),
					to = text_num,
					status_callback = "http://www.roboremindme.ngrok.io/sms_to_db"
					)
	else:
		send_date = datetime.now()
		message = client.messages \
				.create(
					body = "msg",
					from_= twilio("twilio_num"),
					to = text_num,
					status_callback = "http://www.roboremindme.ngrok.io/sms_to_db"
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
def sms_to_db():
	"""Adds text data to db, Twilio sends info here when text is initiated"""
	pass

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
	app.run(debug=True, host="0.0.0.0")