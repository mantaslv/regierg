import re
from datetime import time, datetime

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

def correct_total_time_if_needed(total_time, row_time):
    time_format = "%H:%M:%S.%f"

    if total_time is not None and total_time < row_time:
        incorrect_total_time_str = total_time.strftime(time_format)
        row_time_str = row_time.strftime(time_format)

        incorrect_total_time_list = list(incorrect_total_time_str)

        for index, char in enumerate(incorrect_total_time_list):
            if char == "2" and row_time_str[index] == "3":
                incorrect_total_time_list[index] = "3" 

        corrected_total_time_str = ''.join(incorrect_total_time_list)

        return datetime.strptime(corrected_total_time_str, time_format).time()
    return total_time
