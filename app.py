from datetime import datetime, time
import json
import re

class ErgSession:
	def __init__(self):
		self.monitor_model = None
		self.date = None
		self.session_name = None
		self.total_time = None
	
	def to_json(self):
		return json.dumps({
			"monitor_model": self.monitor_model,
			"date": self.date.strftime('%Y-%m-%d') if self.date else None,
			"session_name": self.session_name,
			"total_time": self.total_time.strftime('%H:%M:%S.%f')
		}, indent=4)
    
def parse_erg_data(data):
	session = ErgSession()

	for index, item in enumerate(data):
		if 'PM' in item:
			session.monitor_model = item
		elif re.match(r'\w+ \d+ \d{4}', item):
			session.date = datetime.strptime(item, '%b %d %Y')
		elif 'View Detail' in item:
			session.session_name = data[index + 1]
		elif 'Total Time:' in item:
			time_str = data[index + 2]
			minutes, seconds = time_str.split(':')
			seconds, milliseconds = seconds.split('.')
			minutes = int(minutes)
			seconds = int(seconds)
			milliseconds = int(float('0.' + milliseconds) * 1000000)
			t = time(hour=0, minute=minutes, second=seconds, microsecond=milliseconds)
			session.total_time = t
			

	return session

data = ['Oconcept 2', 'PM5', 'View Detail', '5x6:00/2:00r', 'Total Time:', 'Apr 18 2024', '40:00.0', 'time meter', '1500m', '30:00.0', '8482', '1:46.1 21', '6:00.0', '1627', '1:50.6 20 150', '6:00.0', '1677 1:47.3 21 161', '6:00.0', '1736', '1:43.6 23 169', '6:00.0', '1718. 1:44.7 22 171', '6:00.0', '1723 1:44.4 22 180', 'r245', 'Units', 'Display', 'Menu']
session = parse_erg_data(data)
json_output = session.to_json()
print(json_output)