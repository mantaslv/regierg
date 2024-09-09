from regierg.utils.parsing_helpers import (
    clean_date, clean_time_or_number, string_to_time, correct_total_time_if_needed, remove_leading_zeros_from_time, subtract_times, generate_session_name_if_none
)
from regierg.models.erg_session import ErgSession, IntervalData
from datetime import datetime, time
import json
import re

CUSTOM_INTERVAL_PATTERN = re.compile(r'¥.*? Total Time:')
MONITOR_MODEL_PATTERN = re.compile(r'(PM\d)')
DATE_PATTERN = re.compile(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.:]? \d{1,2}[.:]? \d{4})')
TIME_PATTERN = re.compile(r'(\d+[:1]\d+[.,]\d+)')
METERS_PATTERN = re.compile(r'(\d+\.?\d*m?)')
REST_PATTERN = re.compile(r'([Fr7][1-9]?[1:][0-5][0-9])')
SESSION_NAME_PATTERN = re.compile(r'(\d+x\d{1,4}m[/)]\d{1,2}:\d{2}r|\d{1,4}m|\d{1,2}:\d{2}|\d+x\d{1,2}:\d{2}/\d{1,2}:\d{2}r)')
VIEW_DETAIL_TITLE_PATTERN = re.compile(r'(Detail)')
TOTAL_TIME_TITLE_PATTERN = re.compile(r'(Total Time)')
RATE_PATTERN = re.compile(r'(\d+)')

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

    def remove_matched_part(match_object): # to process the string sequentially
        nonlocal data_seq
        data_seq = data_seq[match_object.end():].strip()
    
    def match_and_remove(pattern):
        match = pattern.search(data_seq)
        if match:
            remove_matched_part(match)
            return match.group(0)
        return None

    is_interval_workout = False
    is_custom_interval_workout = False
    is_distance_custom_interval = False

    session.monitor_model = match_and_remove(MONITOR_MODEL_PATTERN)
    match_and_remove(VIEW_DETAIL_TITLE_PATTERN)
    
    match = CUSTOM_INTERVAL_PATTERN.search(data_seq)
    if match:
        is_custom_interval_workout = True
        if "m" in match.group(0):
            is_distance_custom_interval = True
    else:
        match = SESSION_NAME_PATTERN.search(data_seq.split(' ', 1)[0])
        if match:
            session.session_name = match.group(0).replace(")", "/").strip(':.')

    total_time_match = match_and_remove(TOTAL_TIME_TITLE_PATTERN)
    if total_time_match:
        is_interval_workout = True
    
    date_match = match_and_remove(DATE_PATTERN)
    if date_match:
        session.date = datetime.strptime(clean_date(date_match), '%b %d %Y')
    else:
        session.date = metadata_date
    
    if is_interval_workout:
        total_time_match = match_and_remove(TIME_PATTERN)
        if total_time_match:
            cleaned_time = clean_time_or_number(total_time_match)
            session.total_time = string_to_time(cleaned_time)

    row_time_match = match_and_remove(TIME_PATTERN)
    if row_time_match:
        session.row_time = string_to_time(clean_time_or_number(row_time_match))
    
    if not is_interval_workout:
        session.total_time = session.row_time

    meters_match = match_and_remove(METERS_PATTERN)
    if meters_match:
        cleaned_meters = clean_time_or_number(meters_match).replace('m', '')
        session.meters = cleaned_meters

    average_split_match = match_and_remove(TIME_PATTERN)
    if average_split_match:
        session.average_split = clean_time_or_number(average_split_match)

    average_rate_match = match_and_remove(RATE_PATTERN)
    if average_rate_match:
        session.average_rate = clean_time_or_number(average_rate_match)
        
    

    def parse_interval():
        nonlocal data_seq
        interval = IntervalData()

        print("\n", data_seq)
        duration_match = match_and_remove(TIME_PATTERN)
        print(duration_match)
        if duration_match:
            interval.duration = string_to_time(clean_time_or_number(duration_match))

        match = match_and_remove(METERS_PATTERN)
        if match:
            cleaned_meters = clean_time_or_number(match).replace('m', '')
            interval.meters = int(cleaned_meters)

        match = match_and_remove(TIME_PATTERN)
        if match:
            cleaned_split_time = clean_time_or_number(match)
            interval.split_time = cleaned_split_time

        match = match_and_remove(RATE_PATTERN)
        if match:
            cleaned_stroke_rate = clean_time_or_number(match)
            interval.stroke_rate = int(cleaned_stroke_rate)

        # Check that no letter precedes the number which may indicate it is part of rest meters
        print("\n", data_seq)
        match = re.search(r'(?<![a-zA-Z:])\b\d+\b', data_seq) 
        print(match)
        if match:
            # Check if the matched number is followed by a colon, indicating it might be part of a time
            next_part = data_seq[match.end():].strip()
            if not next_part.startswith(':'):
                cleaned_heart_rate = clean_time_or_number(match.group(0))
                interval.heart_rate = int(cleaned_heart_rate)
                remove_matched_part(match)

        if is_custom_interval_workout:
            match = match_and_remove(REST_PATTERN)
            if match:
                cleaned_rest = match[:-3] + ":" + match[-2:]
                cleaned_rest = cleaned_rest[1:]
                if len(cleaned_rest) == 3:
                    cleaned_rest = "0" + cleaned_rest 
                interval.rest = cleaned_rest

        return interval if interval.is_valid() else None

    while True:
        interval = parse_interval()

        if not interval:
            break
        session.add_interval(interval)

    session.total_time = correct_total_time_if_needed(session.total_time, session.row_time)

    if is_custom_interval_workout:
        if all(interval["rest"] == "0:00" for interval in session.intervals):
            session.session_name = session.meters + "m"
        else:
            session_name = []
            for interval in session.intervals:
                session_name.append(remove_leading_zeros_from_time(str(interval["duration"])))
                session_name.append(str(interval["rest"]) + "r")
            session_name.pop()
            session.session_name = "/".join(session_name)
    else:
        generate_session_name_if_none(session)

    return session