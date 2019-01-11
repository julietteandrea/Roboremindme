
# Helpful functions to remove clutter from main file

from datetime import datetime
from dateutil import tz
from pytz import timezone

#################### functions #####################

def convertlocal_utc(send_date, timezone):
	""" Converts time user inputs to utc."""
	
	# Auto-detect zones:
	from_zone = tz.gettz(timezone)
	to_zone = tz.tzutc()
	print("from zone = {}".format(from_zone.tzname(datetime.now())))
	print("to zone = {}".format(to_zone.tzname(datetime.now())))

	# est = datetime.'local'now()
	est = datetime.strptime(send_date, '%Y-%m-%d %H:%M:%S')

	# Tell datetime object it's in local time zone
	est = est.replace(tzinfo=from_zone)
	
	utc_time = est.astimezone(to_zone)
	print("convert to utcfffffff")
	return datetime.strftime(utc_time,'%Y-%m-%d %H:%M:%S')
def convert2_24(time):
	""" Converts standard time format to 24 hours."""
	
	# Check if last two elements are PM, then add 12 to hour. If AM then 
	# don't add. Remove tz.

	if time[-2:] == "AM" and time[0:2] == "12":
		return "00" + time[2:8]
	
	elif time[-2:] == "AM":
		return time[0:8]
	
	elif time[-2:] == "PM" and time[0:2] == "12":
		return time[0:8]
	
	else:
		return str(int(time[:2]) + 0) + time[2:8]


		

