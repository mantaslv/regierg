from datetime import time
import json
from regierg.utils.parsing_helpers import remove_leading_zeros_from_time

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
    
    def add_interval(self, interval):
        self.intervals.append({
            "duration": interval.duration,
            "meters": interval.meters,
            "split_time": interval.split_time,
            "stroke_rate": interval.stroke_rate,
            "heart_rate": interval.heart_rate,
            "rest": interval.rest
        })
    
    def format_time_with_decimal(self, time_value):
        if time_value is None:
            return None
        if type(time_value) == str:
            return time_value
        return time_value.strftime('%H:%M:%S.') + f'{time_value.microsecond / 1_000_000:.1f}'[2:]

    def to_json(self):
        return json.dumps({
            "monitor_model": self.monitor_model,
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "session_name": self.session_name,
            "total_time": self.format_time_with_decimal(self.total_time),
            "row_time": self.format_time_with_decimal(self.row_time),
            "meters": self.meters,
            "average_split": remove_leading_zeros_from_time(self.format_time_with_decimal(self.average_split)),
            "average_rate": self.average_rate,
            "intervals": [
                {
                    "duration": self.format_time_with_decimal(interval["duration"]),
                    "meters": interval["meters"],
                    "split_time": remove_leading_zeros_from_time(self.format_time_with_decimal(interval["split_time"])),
                    "stroke_rate": interval["stroke_rate"],
                    "heart_rate": interval["heart_rate"],
                    "rest": interval["rest"]
                } for interval in self.intervals
            ]
        }, indent=4)

class IntervalData:
    def __init__(self, duration=None, meters=None, split_time=None, stroke_rate=None, heart_rate=None, rest=None):
        self.duration = duration
        self.meters = meters
        self.split_time = split_time
        self.stroke_rate = stroke_rate
        self.heart_rate = heart_rate
        self.rest = rest

    def is_valid(self):
        return self.stroke_rate is not None and self.meters is not None