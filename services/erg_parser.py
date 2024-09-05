from regierg.utils.parsing_helpers import (
    clean_date, clean_time_or_number, string_to_time, correct_total_time_if_needed, remove_leading_zeros_from_time, subtract_times, generate_session_name_if_none
)
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
    metadata_date = data["metadata_date"]
    raw_screen_text = data["raw_screen_text"]
    data_str = ' '.join(raw_screen_text)
    data_seq = data_str

    custom_interval_pattern = re.compile(r'(\.{3})')
    monitor_model_pattern = re.compile(r'(PM\d)')
    date_pattern = re.compile(r'(\w+[.:]? \d{1,2}[.:]? \d{4})')
    time_pattern = re.compile(r'(\d+[:1]\d+[.,]\d+)')
    meters_pattern = re.compile(r'(\d+\.?\d*m?)')
    rest_pattern = re.compile(r'([r7][1-9]?:[0-5][05])')
    session_name_pattern = re.compile(r'(\d+x\d{1,4}m[/)]\d{1,2}:\d{2}r|\d{1,4}m|\d{1,2}:\d{2}|\d+x\d{1,2}:\d{2}/\d{1,2}:\d{2}r)')
    
    def remove_matched_part(match): # to process the string sequentially
        nonlocal data_seq
        match_start = data_seq.find(match)
        data_seq = data_seq[match_start + len(match):].strip()
    
    match = monitor_model_pattern.search(data_seq)
    if match:
        session.monitor_model = match.group(1)
        remove_matched_part(match.group(0))
    
    if 'Detail' in data_seq:
        remove_matched_part('Detail')
    
    is_custom_interval_workout = False

    match = custom_interval_pattern.search(data_seq)
    if match:
        is_custom_interval_workout = True
    else:
        match = session_name_pattern.search(data_seq.split(' ', 1)[0])
        if match:
            session.session_name = match.group(0).replace(")", "/").strip(':.')
            remove_matched_part(match.group(0))
    
    is_interval_workout = False

    if 'Total Time' in data_seq:
        is_interval_workout = True
        remove_matched_part('Total Time')
    
    match = date_pattern.search(data_seq)
    if match:
        cleaned_date = clean_date(match.group(0))
        try:
            session.date = datetime.strptime(cleaned_date, '%b %d %Y')
        except ValueError:
            print(f"Failed to parse date: {cleaned_date}")
        remove_matched_part(match.group(0))

    if not session.date:
        session.date = metadata_date
    
    if is_interval_workout:
        match = time_pattern.search(data_seq)
        if match:
            cleaned_time = clean_time_or_number(match.group(0))
            session.total_time = string_to_time(cleaned_time)
            remove_matched_part(match.group(0))
    
    match = time_pattern.search(data_seq)
    if match:
        cleaned_time = clean_time_or_number(match.group(0))
        session.row_time = string_to_time(cleaned_time)
        remove_matched_part(match.group(0))
    
    if not is_interval_workout:
        session.total_time = session.row_time
    
    match = meters_pattern.search(data_seq)
    if match:
        cleaned_meters = clean_time_or_number(match.group(0)).replace('m', '')
        session.meters = cleaned_meters
        remove_matched_part(match.group(0))
    
    match = time_pattern.search(data_seq)
    if match:
        cleaned_split = clean_time_or_number(match.group(0))
        session.average_split = cleaned_split
        remove_matched_part(match.group(0))
    
    match = re.search(r'\d+', data_seq)
    if match:
        cleaned_rate = clean_time_or_number(match.group(0))
        session.average_rate = cleaned_rate
        remove_matched_part(match.group(0))

    while True:
        duration = None
        meters = None
        split_time = None
        stroke_rate = None
        heart_rate = None
        rest = None

        match = time_pattern.search(data_seq)
        if match:
            cleaned_duration = clean_time_or_number(match.group(0))
            duration = string_to_time(cleaned_duration)
            remove_matched_part(match.group(0))
        else:
            break  # no more intervals found

        match = meters_pattern.search(data_seq)
        if match:
            cleaned_meters = clean_time_or_number(match.group(0)).replace('m', '')
            meters = int(cleaned_meters)
            remove_matched_part(match.group(0))

        match = time_pattern.search(data_seq)
        if match:
            cleaned_split_time = clean_time_or_number(match.group(0))
            split_time = cleaned_split_time
            remove_matched_part(match.group(0))

        match = re.search(r'\d+', data_seq)
        if match:
            cleaned_stroke_rate = clean_time_or_number(match.group(0))
            stroke_rate = int(cleaned_stroke_rate)
            remove_matched_part(match.group(0))

        # Check that no letter precedes the number which may indicate it is part of rest meters
        match = re.search(r'(?<![a-zA-Z:])\b\d+\b', data_seq) 
        if match:
            # Check if the matched number is followed by a colon, indicating it might be part of a time
            next_part = data_seq[match.end():].strip()
            if not next_part.startswith(':'):
                cleaned_heart_rate = clean_time_or_number(match.group(0))
                heart_rate = int(cleaned_heart_rate)
                remove_matched_part(match.group(0))

        if is_custom_interval_workout:
            match = rest_pattern.search(data_seq)
            print(match)
            if match:
                cleaned_rest = clean_time_or_number("0" + match.group(0)[1:])
                print(cleaned_rest)
                rest = cleaned_rest
                remove_matched_part(match.group(0))

        session.add_interval(duration, meters, split_time, stroke_rate, heart_rate, rest)

    session.total_time = correct_total_time_if_needed(session.total_time, session.row_time)

    if is_custom_interval_workout:
        if all(interval["rest"] == "0:00" for interval in session.intervals):
            session.session_name = session.meters + "m"
    else:
        generate_session_name_if_none(session)

    return session