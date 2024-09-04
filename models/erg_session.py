from datetime import time
import json

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
    
    def format_time_with_decimal(self, time_value):
        if time_value is None:
            return None
        return time_value.strftime('%H:%M:%S.') + f'{time_value.microsecond / 1_000_000:.1f}'[2:]

    def to_json(self):
        return json.dumps({
            "monitor_model": self.monitor_model,
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "session_name": self.session_name,
            "total_time": self.format_time_with_decimal(self.total_time),
            "row_time": self.format_time_with_decimal(self.row_time),
            "meters": self.meters,
            "average_split": self.average_split,
            "average_rate": self.average_rate,
            "intervals": [
                {
                    "duration": self.format_time_with_decimal(interval["duration"]),
                    "meters": interval["meters"],
                    "split_time": interval["split_time"],
                    "stroke_rate": interval["stroke_rate"],
                    "heart_rate": interval["heart_rate"]
                } for interval in self.intervals
            ]
        }, indent=4)