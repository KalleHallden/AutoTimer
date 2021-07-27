import json
from collections import defaultdict

from dateutil import parser


class ActivityList:
    def __init__(self, filename=None):
        self.activities = defaultdict(list) if filename is None else self.load(filename)

    def load(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return defaultdict(list)
        if not data:
            return defaultdict(list)
        activities = defaultdict(list)
        for activity in data['activities']:
            time_entries = self.get_time_entries_from_json(activity['time_entries'])
            activities[activity['name']].extend(time_entries)
        return activities

    def write(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.serialize(), json_file, indent=4, sort_keys=True)

    @staticmethod
    def get_time_entries_from_json(time_entries):
        return_list = []
        for entry in time_entries:
            return_list.append(
                TimeEntry(
                    start_time=parser.parse(entry['start_time']),
                    end_time=parser.parse(entry['end_time']),
                    days=entry['days'],
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds'],
                )
            )
        return return_list
    
    def serialize(self):
        d = {'activities': []}
        for name, time_entries in self.activities.items():
            entry = {'name': name, 'time_entries': [t.serialize() for t in time_entries]}
            d['activities'].append(entry)
        return d

    # def append(self, activities):
    #     for a in self.activities:
    #         if a.name in


class TimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds, specific=False):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        if specific:
            self.get_specific_times()
    
    def get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }
