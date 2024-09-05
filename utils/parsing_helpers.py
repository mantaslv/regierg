import re
from datetime import time

def clean_time_or_number(value):
    # Remove trailing or leading dots or colons around numbers and time formats
    value = value.replace(",", ".")
    return re.sub(r'^[.:]+|[.:]+$', '', value)

def clean_date(value):
    # Remove leading/trailing dots or colons and clean each part of the date
    parts = value.split()
    cleaned_parts = [re.sub(r'^[.:]+|[.:]+$', '', part) for part in parts]
    cleaned_date = ' '.join(cleaned_parts)
    return cleaned_date

def string_to_time(time_str):
    minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split('.')
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(float('0.' + milliseconds) * 1000000)
    t = time(hour=0, minute=minutes, second=seconds, microsecond=milliseconds)
    return t
