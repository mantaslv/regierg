from regierg.utils.parsing_helpers import clean_date_str, clean_session_name, clean_rest, remove_m, str_to_date, clean_num_time, str_to_time, correct_total_time_if_needed, remove_leading_zeros_from_time, subtract_times, generate_custom_interval_session_name, generate_session_name_if_none
from regierg.models.erg_session import ErgSession, IntervalData
from datetime import datetime
import json
import re

CUSTOM_INTERVAL_PATTERN = re.compile(r'[¥v].*? Total Time:')
MONITOR_MODEL_PATTERN = re.compile(r'(PM\d)')
DATE_PATTERN = re.compile(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[.:]? \d{1,2}[.:]? \d{4})')
TIME_PATTERN = re.compile(r'(\d+[:1]\d+[.,]\d+)')
METERS_PATTERN = re.compile(r'(\d{3,}\.?\d*m?)')
REST_PATTERN = re.compile(r'([Fr7¥1][1-9]?[1:][0-5][0-9])')
SESSION_NAME_PATTERN = re.compile(r'(\d+x\d{1,4}m[/)]\d{1,2}:\d{2}r|\d{1,4}m|\d{1,2}:\d{2}|\d+x\d{1,2}:\d{2}/\d{1,2}:\d{2}r)')
VIEW_DETAIL_TITLE_PATTERN = re.compile(r'(Detail)')
TOTAL_TIME_TITLE_PATTERN = re.compile(r'(Total Time)')
RATE_PATTERN = re.compile(r'(\d+)')
INTERVAL_HR_PATTERN = re.compile(r'((?<![a-zA-Z:])\b\d+\b)')

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

    def remove_matched_part(match_object):
        nonlocal data_seq
        data_seq = data_seq[match_object.end():].strip()
    
    def extract_clean_from_seq(pattern, *cleaners, search_first_part=False):
        nonlocal data_seq
        search_area = data_seq.split(' ', 1)[0] if search_first_part else data_seq
        match = pattern.search(search_area)
        if match:
            matched_text = match.group(0)

            for cleaner in cleaners:
                matched_text = cleaner(matched_text)
                if matched_text is None:
                    return None

            remove_matched_part(match)
            return matched_text
        return None

    # Extract monitor model and other basic data
    session.monitor_model = extract_clean_from_seq(MONITOR_MODEL_PATTERN)
    extract_clean_from_seq(VIEW_DETAIL_TITLE_PATTERN)
    
    # Custom interval workout check
    match = CUSTOM_INTERVAL_PATTERN.search(data_seq)
    is_custom_interval_workout = bool(match)
    is_distance_custom_interval = "m" in match.group(0)[:-3] if match else False

    # Standard session name if not custom interval
    if not is_custom_interval_workout:
        print("is not custom interval")
        session.session_name = extract_clean_from_seq(SESSION_NAME_PATTERN, clean_session_name, search_first_part=True)

    # Interval workout check
    is_interval_workout = extract_clean_from_seq(TOTAL_TIME_TITLE_PATTERN) is not None
    
    # Date handling
    session.date = extract_clean_from_seq(DATE_PATTERN, clean_date_str, str_to_date) or metadata_date
    
    # Time handling
    if is_interval_workout:
        session.total_time = extract_clean_from_seq(TIME_PATTERN, clean_num_time, str_to_time)

    session.row_time = extract_clean_from_seq(TIME_PATTERN, clean_num_time, str_to_time)
    
    if not is_interval_workout:
        session.total_time = session.row_time

    # Meters, split, and rate
    session.meters = extract_clean_from_seq(METERS_PATTERN, clean_num_time, remove_m, int)
    session.average_split = extract_clean_from_seq(TIME_PATTERN, clean_num_time)
    session.average_rate = extract_clean_from_seq(RATE_PATTERN, clean_num_time, int)

    def check_next_part_not_time(matched_text):
        next_part = data_seq[data_seq.find(matched_text) + len(matched_text):].strip()
        if next_part.startswith(':'):  
            return None
        return matched_text
        
    def parse_interval():
        nonlocal data_seq
        interval = IntervalData()

        print(data_seq)

        interval.duration = extract_clean_from_seq(TIME_PATTERN, clean_num_time, str_to_time)
        interval.meters = extract_clean_from_seq(METERS_PATTERN, clean_num_time, remove_m, int)
        interval.split_time = extract_clean_from_seq(TIME_PATTERN, clean_num_time)
        interval.stroke_rate = extract_clean_from_seq(RATE_PATTERN, clean_num_time, int)
        interval.heart_rate = extract_clean_from_seq(INTERVAL_HR_PATTERN, check_next_part_not_time, clean_num_time, int)
        if is_custom_interval_workout:            
            interval.rest = extract_clean_from_seq(REST_PATTERN, clean_rest)

        return interval if interval.is_valid() else None
    
    # Parse intervals
    while True:
        interval = parse_interval()
        if not interval:
            break
        session.add_interval(interval)

    # Correct total time if needed
    session.total_time = correct_total_time_if_needed(session.total_time, session.row_time)

    # Generate session name
    if is_custom_interval_workout:
        session.session_name = generate_custom_interval_session_name(session, is_distance_custom_interval)
    else:
        session.session_name = generate_session_name_if_none(session)

    return session