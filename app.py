from flask import Flask, request, render_template, flash, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import datetime
from config import *

app = Flask(__name__)

account_sid = account_sid("account_num")
auth_token = auth_token("token_num")

client = Client(account_sid, auth_token)
#It's a great thing when you realize you still have the ability to surprise yourself. 
# "Now, a question of etiquette - as I pass, do I give you the ass or the crotch? Now, a question of etiquette - as I pass, do I give you the ass or the crotch? ",

@app.route("/sms")
def index():
	"""displays homepage"""
	return render_template("homepage.html")

#Refactor
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
	else:
		send_time = time
	# send_date = request.form.get("")
	sendnow = request.form.get("textrn")
	if sendnow:
		message = client.messages \
				.create(
					body = msg,
					from_= twilio("twilio_num"),
					to = text_num
					)
	else:
		message = client.messages \
				.create(
					body = "this gets saved for a later time",
					from_= twilio("twilio_num"),
					to = text_num
					)
	# save to, time created, time sent, message, sid insiide the database.
	print("time = {}".format(send_time))
	print(message)#message is a class
	print(datetime.datetime.now())
	print("message sid = {}".format(message.sid))
	print("message recipent = {}".format(message.to))
	print("message created = {}".format(message.date_created))
	print("message sent = {}".format(message.date_sent))
	print("message body = {}".format(message.body))

	return redirect("/sms")

# @app.route("/resp", methods=['GET', 'POST'])
# def sms_ahoy_reply():
# 	"""Respond to incoming messages with a friendly SMS."""
# 	# a way to check what the reply was before sending a response. responsd will be based on the 'body'
# 	# of the reply. example: 'stop' = opt out. or redo the reminder for tomorrow instead or 
# 	# a simple thank you and you're welcome response.

# 	# Start our response
# 	resp = MessagingResponse()

# 	# Add a message
# 	resp.message("I'm on it.")

# 	print()

	# return str(resp)

@app.route("/resp", methods=['GET', 'POST'])
def sms_reply():
	"""Send a dynamic reply to an incoming text message."""
	# Get the message the user sent our app number
	body = request.values.get('Body', None)

	# Start our TwiML response
	resp = MessagingResponse()

	# Determine the right reply for this message
	body =body.lower()
	if body == 'remove':
		resp.message("")
	

	return str(resp)


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")