from flask import Flask, request, render_template, flash, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from datetime import date
from config import *

app = Flask(__name__)

account_sid = account_sid("account_num")
auth_token = auth_token("token_num")

client = Client(account_sid, auth_token)
#It's a great thing when you realize you still have the ability to surprise yourself. 
# "Now, a question of etiquette - as I pass, do I give you the ass or the crotch? ",

@app.route("/sms")
def index():
	"""displays homepage"""
	return render_template("homepage.html")

@app.route("/sms", methods=["GET", "POST"])
def testing_homepage():
	text_num = request.form.get("phone")
	msg = request.form.get("reminder")
	# send_time = request.form.get("")
	# send_date = request.form.get("")
	message = client.messages \
				.create(
					body = msg,
					from_= twilio("twilio_num"),
					to = text_num
					)
	#save to, time created, time sent, message, sid insiide the database.
	print(message)#message is a class
	print("message sid = {}".format(message.sid))
	print("message recipent = {}".format(message.to))
	print("message created = {}".format(message.date_created))
	print("message sent = {}".format(message.date_sent))
	print("message body = {}".format(message.body))

	return redirect("/sms")

@app.route("/resp", methods=['GET', 'POST'])
def sms_ahoy_reply():
	"""Respond to incoming messages with a friendly SMS."""
	#a way to check what the reply was before sending a response. responsd will be based on the 'body'
	#of the reply. example: 'stop' = opt out. or redo the reminder for tomorrow instead or 
	#a simple thank you and you're welcome response.

	#Start our response
	resp = MessagingResponse()

	#Add a message
	resp.message("I'm on it.")

	print()

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")