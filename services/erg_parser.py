from regierg.utils.parsing_helpers import clean_date, clean_time_or_number, string_to_time
from regierg.models.erg_session import ErgSession
from datetime import datetime, time
import json
import re

def serialize_erg_data(data):
    session = parse_erg_data(data)
    json_output = session.to_json()
    return json_output

def parse_erg_data(data):
    session = ErgSession()

    # Join the data into a single string
    data_str = ' '.join(data)

    data_seq = data_str

    # Define the search patterns
    monitor_model_pattern = re.compile(r'(PM\d)')
    date_pattern = re.compile(r'(\w+[.:]? \d{1,2}[.:]? \d{4})')
    time_pattern = re.compile(r'(\d+:\d+\.\d+)')
    meters_pattern = re.compile(r'(\d+\.?\d*m?)')
    
    # Process the string sequentially
    def remove_matched_part(match):
        nonlocal data_seq
        match_start = data_seq.find(match)
        data_seq = data_seq[match_start + len(match):].strip()
    
    # Monitor Model
    match = monitor_model_pattern.search(data_seq)
    if match:
        session.monitor_model = match.group(1)
        remove_matched_part(match.group(0))
    
    # View Detail
    if 'Detail' in data_seq:
        remove_matched_part('Detail')
    
    # Session Name
    match = re.search(r'[^\s]+', data_seq)
    if match:
        session.session_name = match.group(0).strip(':.')
        remove_matched_part(match.group(0))
    
    is_interval_workout = False

    # Total Time Label
    if 'Total Time:' in data_seq:
        is_interval_workout = True
        remove_matched_part('Total Time:')
    
    # Date
    match = date_pattern.search(data_seq)
    if match:
        cleaned_date = clean_date(match.group(0))
        try:
            session.date = datetime.strptime(cleaned_date, '%b %d %Y')
        except ValueError:
            print(f"Failed to parse date: {cleaned_date}")
        remove_matched_part(match.group(0))
    
    # Total Time
    if is_interval_workout:
        match = time_pattern.search(data_seq)
        if match:
            cleaned_time = clean_time_or_number(match.group(0))
            session.total_time = string_to_time(cleaned_time)
            remove_matched_part(match.group(0))
    
    # Remove "time meter"
    match = re.search(r'time meter \S+', data_seq)
    if match:
        remove_matched_part(match.group(0))
    
    # Row Time
    match = time_pattern.search(data_seq)
    if match:
        cleaned_time = clean_time_or_number(match.group(0))
        session.row_time = string_to_time(cleaned_time)
        remove_matched_part(match.group(0))
    
    if not is_interval_workout:
        session.total_time = session.row_time
    
    # Meters
    match = meters_pattern.search(data_seq)
    if match:
        cleaned_meters = clean_time_or_number(match.group(0)).replace('m', '')
        session.meters = cleaned_meters
        remove_matched_part(match.group(0))
    
    # Average Split
    match = time_pattern.search(data_seq)
    if match:
        cleaned_split = clean_time_or_number(match.group(0))
        session.average_split = cleaned_split
        remove_matched_part(match.group(0))
    
    # Average Rate
    match = re.search(r'\d+', data_seq)
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
        match = time_pattern.search(data_seq)
        if match:
            cleaned_duration = clean_time_or_number(match.group(0))
            duration = string_to_time(cleaned_duration)
            remove_matched_part(match.group(0))
        else:
            break  # No more intervals found

        # Meters
        match = meters_pattern.search(data_seq)
        if match:
            cleaned_meters = clean_time_or_number(match.group(0)).replace('m', '')
            meters = int(cleaned_meters)
            remove_matched_part(match.group(0))

        # Split Time
        match = time_pattern.search(data_seq)
        if match:
            cleaned_split_time = clean_time_or_number(match.group(0))
            split_time = cleaned_split_time
            remove_matched_part(match.group(0))

        # Stroke Rate
        match = re.search(r'\d+', data_seq)
        if match:
            cleaned_stroke_rate = clean_time_or_number(match.group(0))
            stroke_rate = int(cleaned_stroke_rate)
            remove_matched_part(match.group(0))

        # Heart Rate
        match = re.search(r'(?<![a-zA-Z])\b\d+\b', data_seq) # Check that no letter precedes the number which may indicate it is part of rest meters
        if match:
            # Check if the matched number is followed by a colon, indicating it might be part of a time
            next_part = data_seq[match.end():].strip()
            if not next_part.startswith(':'):
                cleaned_heart_rate = clean_time_or_number(match.group(0))
                heart_rate = int(cleaned_heart_rate)
                remove_matched_part(match.group(0))


        # Add the interval to the session
        session.add_interval(duration, meters, split_time, stroke_rate, heart_rate)

    return session