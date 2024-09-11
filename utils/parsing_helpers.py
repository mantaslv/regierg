import re
from datetime import time, datetime

def clean_num_time(value):
    # Remove trailing or leading dots or colons around numbers and time formats
    value = value.replace(",", ".")
    return re.sub(r'^[.:]+|[.:]+$', '', value)

def clean_date_str(value):
    # Remove leading/trailing dots or colons and clean each part of the date
    parts = value.split()
    cleaned_parts = [re.sub(r'^[.:]+|[.:]+$', '', part) for part in parts]
    cleaned_date = ' '.join(cleaned_parts)
    return cleaned_date

def str_to_date(value):
    return datetime.strptime(value, '%b %d %Y')

def remove_m(value):
     return value.replace('m', '')

def clean_rest(value):
    rest = value[:-3] + ":" + value[-2:]    # colon correction
    rest = rest[1:]                         # remove rest indication letter
    if len(rest) == 3:
        rest = "0" + rest                   # add 0 before colon if required
    return rest

def clean_session_name(value):
    return value.replace(")", "/").strip(':.')

def str_to_time(time_str):
    minutes = time_str[:-5]
    seconds = time_str[-4:-2]
    milliseconds = time_str[-1]

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

def remove_leading_zeros_from_time(time):
    time_parts = time.split(':')

    if time_parts[0] == "0" or time_parts[0] == "00":
        time_parts.pop(0)
        print(time_parts)
        
        if time_parts[0] == "00":
            time_parts.pop(0)
    
    cleaned_time_parts = [str(int(part)) for part in time_parts]
    cleaned_time_str = ':'.join(cleaned_time_parts)
    if cleaned_time_str[-2] == ":":
        cleaned_time_str += "0"
        
    return cleaned_time_str

def subtract_times(time1, time2):
    datetime1 = datetime.combine(datetime.today(), time1)
    datetime2 = datetime.combine(datetime.today(), time2)
    return datetime1 - datetime2

def generate_session_name_if_none(session):
    if session.session_name is None:
        number_of_intervals = len(session.intervals)

        if session.total_time > session.row_time:
            total_rest = subtract_times(session.total_time, session.row_time)
            rest = remove_leading_zeros_from_time(str(total_rest / number_of_intervals))

            if session.intervals[0]["duration"] == session.intervals[1]["duration"]:
                interval = session.intervals[0]["duration"]
            else:
                interval = str(session.intervals[0]["meters"]) + "m"

            return f"{number_of_intervals}x{interval}/{rest}r"
        else:
            if session.intervals[-1]["meters"] / number_of_intervals == session.intervals[0]["meters"]:
                return f"{session.meters}m"
            else:
                session_name = remove_leading_zeros_from_time(str(session.row_time))
                if len(session_name.split(":")[-1]) == 1:
                    session_name += "0"
                return session_name
    return session.session_name
        
def generate_custom_interval_session_name(session):
    if all(interval["rest"] == "0:00" for interval in session.intervals):
            return str(session.meters) + "m"
    else:
        session_name = []
        for interval in session.intervals:
            session_name.append(remove_leading_zeros_from_time(str(interval["duration"])))
            session_name.append(str(interval["rest"]) + "r")
        session_name.pop()
        return "/".join(session_name)