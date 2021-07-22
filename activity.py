import json
from dateutil import parser


class ActivityList:
    def __init__(self):
        self.activities = []

    def load(self, filename='activities.json'):
        activities = []
        with open(filename, 'r') as f:
            data = json.load(f)
            if not data:
                return activities
            for activity in data['activities']:
                ac = Activity(name=activity['name'], time_entries=self.get_time_entries_from_json(activity))
                activities.append(ac)
        return activities

    def write(self, filename='activities.json'):
        with open(filename, 'w') as json_file:
            json.dump(self.serialize(), json_file, indent=4, sort_keys=True)

    @staticmethod
    def get_time_entries_from_json(data):
        return_list = []
        for entry in data['time_entries']:
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
        return {'activities': [activity.serialize() for activity in self.activities]}

    def by_name(self, activity_name):
        for activity in self.activities:
            if activity.name == activity_name:
                return activity


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {'name': self.name, 'time_entries': [t.serialize() for t in self.time_entries]}
    

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
