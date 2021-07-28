import json
from collections import defaultdict
from datetime import timedelta, datetime

start_date = datetime.strptime('2021-07-27', '%Y-%m-%d')
target_file = 'target.json'
form = '%Y-%m-%d'


def date_range(start, end):
    for n in range(int((end - start).days)):
        yield start + timedelta(n)


class Target:
    # target time in hours
    default = {
        'Programming': 4,
        'AGI book': 1,
        'Thoughts': 1,
    }

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
            self._data[date_str] = history.get(date_str, self.default)

    def write(self):
        with open(target_file, 'w') as json_file:
            json.dump(self._data, json_file, indent=4, sort_keys=True)

    def sum_by_tag(self):
        sum_time = defaultdict(int)
        for goal in self._data.values():
            for tag, hours in goal.items():
                sum_time[tag] += hours
        return sum_time
