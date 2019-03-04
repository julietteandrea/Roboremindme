
##### This file is run by cron every minute #####
from robo import *

def send_scheduled_reminders():
	"""Sends scheduled reminders to client by checking
	the database for reminders with 'pending' status"""
	
	# A list of records with 'pending' status
	status = Reminder.query.filter_by(status='pending').all()
	
	for i in range(len(status)):
		# DB saves the date as a str. Below is converting the str into a datetime
		date_to_send = datetime.strptime(status[i].date_sent, '%Y-%m-%d %H:%M:%S')
		# If date_to_send on 'pending' is equal or less(before) than current time
		if date_to_send <= datetime.now():
			# Retrieve recipient and body
			recipient = status[i].recipent
			msg = status[i].body

			# Data to send to robo.py scheduled_reminders_to_db2
			reminder_id = status[i].message_id
			
			# Send message to client via twilio
			messages = client.messages \
					 .create(
						body=msg,
						from_=app.config['TWILIO_SMSNUM'],
						to=recipient,
						status_callback='http://roboremindme.ngrok.io/modifysms_db/{}'.format(reminder_id)
							)

#send_scheduled_reminders()
