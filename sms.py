from twilio.rest import Client
from config import *

account_sid = account_sid("account_num")
auth_token = auth_token("token_num")

client = Client(account_sid, auth_token)

message = client.messages \
				.create(
					body = " testing 123",
					from_= twilio("twilio_num"),
					to = recipient("recipient_num")
					)
print(message.sid)
print(message.body)
print(message.date_created)
print(message.status)
print(message.to)
print(message.uri)