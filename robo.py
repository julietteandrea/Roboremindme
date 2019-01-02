from flask import Flask, request, render_template, flash, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import datetime
from config import *

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
	text_num = request.form.get("phone")
	msg = request.form.get("reminder")
	time = request.form.get("texttime")
	timezone = request.form.get("timezone")
	if timezone == "pst":
		atime = int(time[:2]) + 8
		send_time = str(atime) + time[2:]
	elif timezone == "est":
		atime = int(time[:2]) + 5
		send_time = str(atime) + time[2:]
	send_date = request.form.get("textdate")
	sendnow = request.form.get("textrn")
	if sendnow:
		message = client.messages \
				.create(
					body = msg,
					from_= twilio("twilio_num"),
					to = text_num,
					status_callback = "http://www.roboremindme.ngrok.io/sms_to_db"
					)
	else:
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
	# save to, time created, time sent, message, sid insiide the database.
	print("time = {}".format(send_time))
	print("date = {}".format(send_date))
	print("message sid = {}".format(message.sid))
	print("message recipent = {}".format(message.to))
	print("message created(now it's current date) = {}".format(datetime.datetime.now()))
	print("message sent date = {}".format(message.date_created))
	print("message sent = {}".format(message.date_sent))
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
	elif "stop" in body:
		resp.message("Until next time then. Goodbye!")
	elif "picture" in body:
		pic = resp.message("Here's my contact picture. Save it under Roboremindme!")
		pic.media("https://c1.staticflickr.com/5/4894/31633985757_1886a7bb04_b.jpg")
	else:
		resp.message("Roboremindme is here to remind you to get things done.")

	

	return str(resp)


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")