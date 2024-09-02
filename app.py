from datetime import datetime, time
import json
import re

class ErgSession:
    def __init__(self):
        self.monitor_model = None
        self.date = None
        self.session_name = None
        self.total_time = None
        self.row_time = None
        self.meters = None
        self.average_split = None
        self.average_rate = None
        self.intervals = []
    
    def add_interval(self, duration, meters, split_time, stroke_rate, heart_rate=None):
        self.intervals.append({
            "duration": duration,
            "meters": meters,
            "split_time": split_time,
            "stroke_rate": stroke_rate,
            "heart_rate": heart_rate
        })
    
    def to_json(self):
        return json.dumps({
            "monitor_model": self.monitor_model,
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "session_name": self.session_name,
            "total_time": self.total_time.strftime('%H:%M:%S') if self.total_time else None,
            "row_time": self.row_time.strftime('%H:%M:%S.%f') if self.row_time else None,
            "meters": self.meters,
            "average_split": self.average_split,
            "average_rate": self.average_rate,
            "intervals": [
                {
                    "duration": interval["duration"].strftime('%H:%M:%S.%f'),
                    "meters": interval["meters"],
                    "split_time": interval["split_time"],
                    "stroke_rate": interval["stroke_rate"],
                    "heart_rate": interval["heart_rate"]
                } for interval in self.intervals
            ]
        }, indent=4)

def clean_time_or_number(value):
    # Remove trailing or leading dots or colons around numbers and time formats
    return re.sub(r'^[.:]+|[.:]+$', '', value)

def clean_date(value):
    # Remove leading/trailing dots or colons and clean each part of the date
    parts = value.split()
    cleaned_parts = [re.sub(r'^[.:]+|[.:]+$', '', part) for part in parts]
    cleaned_date = ' '.join(cleaned_parts)
    return cleaned_date

def parse_erg_data(data):
    session = ErgSession()

    # Join the data into a single string
    data_str = ' '.join(data)

    print(data_str)

    # Define the search patterns
    monitor_model_pattern = re.compile(r'(PM\d)')
    date_pattern = re.compile(r'(\w+[.:]? \d{1,2}[.:]? \d{4})')
    time_pattern = re.compile(r'(\d+:\d+\.\d+)')
    meters_pattern = re.compile(r'(\d+\.?\d*m?)')
    
    # Process the string sequentially
    def remove_matched_part(match):
        nonlocal data_str
        match_start = data_str.find(match)
        data_str = data_str[match_start + len(match):].strip()
    
    # Monitor Model
    match = monitor_model_pattern.search(data_str)
    if match:
        session.monitor_model = match.group(1)
        remove_matched_part(match.group(0))
    
    # View Detail
    if 'View Detail' in data_str:
        remove_matched_part('View Detail')
    
    # Session Name
    match = re.search(r'[^\s]+', data_str)
    if match:
        session.session_name = match.group(0).strip(':.')
        remove_matched_part(match.group(0))
    
    is_interval_workout = False

    # Total Time Label
    if 'Total Time:' in data_str:
        is_interval_workout = True
        remove_matched_part('Total Time:')
    
    # Date
    match = date_pattern.search(data_str)
    if match:
        cleaned_date = clean_date(match.group(0))
        try:
            session.date = datetime.strptime(cleaned_date, '%b %d %Y')
        except ValueError:
            print(f"Failed to parse date: {cleaned_date}")
        remove_matched_part(match.group(0))
    
    # Total Time
    if is_interval_workout:
        match = time_pattern.search(data_str)
        if match:
            cleaned_time = clean_time_or_number(match.group(0))
            session.total_time = string_to_time(cleaned_time)
            remove_matched_part(match.group(0))
    
    # Remove "time meter"
    match = re.search(r'time meter \S+', data_str)
    if match:
        remove_matched_part(match.group(0))
    
    # Row Time
    match = time_pattern.search(data_str)
    if match:
        cleaned_time = clean_time_or_number(match.group(0))
        session.row_time = string_to_time(cleaned_time)
        remove_matched_part(match.group(0))
    
    # Meters
    match = meters_pattern.search(data_str)
    if match:
        cleaned_meters = clean_time_or_number(match.group(0)).replace('m', '')
        session.meters = cleaned_meters
        remove_matched_part(match.group(0))
    
    # Average Split
    match = time_pattern.search(data_str)
    if match:
        cleaned_split = clean_time_or_number(match.group(0))
        session.average_split = cleaned_split
        remove_matched_part(match.group(0))
    
    # Average Rate
    match = re.search(r'\d+', data_str)
    if match:
        cleaned_rate = clean_time_or_number(match.group(0))
        session.average_rate = cleaned_rate
        remove_matched_part(match.group(0))

    # Parsing the intervals
    while True:
        duration = None
        meters = None
        split_time = None
        stroke_rate = None
        heart_rate = None

        # Duration
        match = time_pattern.search(data_str)
        if match:
            cleaned_duration = clean_time_or_number(match.group(0))
            duration = string_to_time(cleaned_duration)
            remove_matched_part(match.group(0))
        else:
            break  # No more intervals found

        # Meters
        match = meters_pattern.search(data_str)
        if match:
            cleaned_meters = clean_time_or_number(match.group(0)).replace('m', '')
            meters = int(cleaned_meters)
            remove_matched_part(match.group(0))

        # Split Time
        match = time_pattern.search(data_str)
        if match:
            cleaned_split_time = clean_time_or_number(match.group(0))
            split_time = cleaned_split_time
            remove_matched_part(match.group(0))

        # Stroke Rate
        match = re.search(r'\d+', data_str)
        if match:
            cleaned_stroke_rate = clean_time_or_number(match.group(0))
            stroke_rate = int(cleaned_stroke_rate)
            remove_matched_part(match.group(0))

        # Heart Rate
        match = re.search(r'\d+', data_str)
        if match:
            # Check if the matched number is followed by a colon, indicating it might be part of a time
            next_part = data_str[match.end():].strip()
            if not next_part.startswith(':'):
                cleaned_heart_rate = clean_time_or_number(match.group(0))
                heart_rate = int(cleaned_heart_rate)
                remove_matched_part(match.group(0))


        # Add the interval to the session
        session.add_interval(duration, meters, split_time, stroke_rate, heart_rate)

    return session

def string_to_time(time_str):
    minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split('.')
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(float('0.' + milliseconds) * 1000000)
    t = time(hour=0, minute=minutes, second=seconds, microsecond=milliseconds)
    return t

data = ['Oconcept 2', 'PM5', 'View Detail', '5x6:00/2:00r.', 'Total Time:', 'Apr 18 2024.', '40:00.0', 'time meter', '1500m', '30:00.0', '8482.', '1:46.1 21', '6:00.0', '1627', '1:50.6 20 150', '6:00.0', '1677 1:47.3 21 161', '6:00.0', '1736', '1:43.6 23 169', '6:00.0', '1718. 1:44.7 22 171', '6:00.0', '1723 1:44.4 22 180', 'r245', 'Units', 'Display', 'Menu']
# data = ['Oconcept 2', 'PM4', 'ROWING', 'View Detail', '2000m', 'Dec. 17 2015', 'time meter', '1500m /m', '6:32.3', '2000 1:38.0 32', '1:14.0', '400 1:32.5 33', '1:18.7', '.800 1:38.3 31', '1:20.7', '1200 1:40.8 31', '1:21.0', '1600 1:41.2 33', '1:17.9', '2000 1:37.3 :35', 'CHANGE', 'UNITS', 'CHANGE', 'DISPLAY', 'MENU', 'BACK']
# data = ['OKconcept 2', 'PM5', 'View Detail', '3x6000m/2:00r', 'Total Time:', 'Feb 14 2019', '1:13:23.7', 'time meter', '1500m', '1:07:23.7', '18000', '1:52.3 20', '22:29.6', '6000', '1:52.4 20', '22:28.5', '6000', '1:52.3 20', '22:25.6', '6000', '1:52.1 20', 'F108', 'Units', 'Display', 'Menu']
session = parse_erg_data(data)
json_output = session.to_json()
print(json_output)
