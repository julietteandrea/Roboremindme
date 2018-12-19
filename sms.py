from twilio.rest import Client
from config import *

account_sid = account_sid("account_num")
auth_token = auth_token("token_num")

client = Client(account_sid, auth_token)
#It's a great thing when you realize you still have the ability to surprise yourself. 

message = client.messages \
				.create(
					body = "Now, a question of etiquette - as I pass, do I give you the ass or the crotch? ",
					from_= twilio("twilio_num"),
					to = recipient("recipient_num")
					)
print(message.sid)
print(message.body)
print(message.date_created)
print(message.status)
print(message.to)
print(message.uri)