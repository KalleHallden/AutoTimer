import json
from collections import defaultdict
from datetime import timedelta, datetime

from config import target_file, start_date, form, default_target


def date_range(start, end):
    for n in range(int((end - start).days)):
        yield start + timedelta(n)


class Target:

    def __init__(self):
        self._data = {}
        try:
            with open(target_file, 'r') as json_file:
                history = json.load(json_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            print(e)
            history = dict()
        for date in date_range(start_date, datetime.today() + timedelta(1)):
            date_str = date.strftime(form)
            self._data[date_str] = history.get(date_str, default_target)

    def write(self):
        with open(target_file, 'w') as json_file:
            json.dump(self._data, json_file, indent=4, sort_keys=True)

    def sum_by_tag(self):
        sum_time = defaultdict(int)
        for goal in self._data.values():
            for tag, hours in goal.items():
                sum_time[tag] += hours
        return sum_time
