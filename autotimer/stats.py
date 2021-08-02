import os
from collections import defaultdict
from datetime import timedelta, datetime

from config import path, tag_to_keys, form
from .target import Target
from .activity import ActivityList


def logged_dates():
    for files in os.listdir(path):
        filename = os.path.join(path, files)
        if not os.path.isfile(filename) or files[:4] != 'log_':
            continue
        yield filename, files[4:-5]


def collect_all_activities():
    """Collect activities from every day."""
    activities = defaultdict(list)
    for filename, _ in logged_dates():
        print('Reading: {}'.format(filename))
        al = ActivityList(filename=filename)
        al.append(activities)
    return activities


class TimerStats:

    def __init__(self):
        self.acts = dict()
        self.keyword_dict = self.get_keyword_dict()

    @staticmethod
    def get_keyword_dict():
        inv_keys = dict()
        for tag, keywords in tag_to_keys.items():
            for key in keywords:
                inv_keys[key] = tag
        return inv_keys

    def order_by_time(self, date_str):
        if date_str not in self.acts or date_str == datetime.today().strftime(form):
            self.acts[date_str] = ActivityList(filename=path + 'log_' + date_str + '.json')
        times = []
        for name, time_entries in self.acts[date_str].acts.items():
            for entry in time_entries:
                s = entry.start_time
                if s.strftime(form) != date_str or entry.end_time.strftime(form) != date_str:
                    continue
                times.append((s, entry.end_time, name))
        return sorted(times, key=lambda x: x[0])

    def times_to_tag_times(self, times):
        """Group activities and their sorted times into times for tags."""
        tag_times = []
        current_tag = ""
        tag_start, tag_end = None, None
        for start, end, activity in times:
            tag = self.activity_to_tag(activity)
            # if tag changes or distance between equal tags is more than 5 seconds, make new tag entry
            if tag != current_tag or tag_end and (start - tag_end).seconds > 30:
                if current_tag != "":
                    tag_times.append((tag_start, tag_end, current_tag))
                current_tag = tag
                tag_start = start
            tag_end = end
        tag_times.append((tag_start, tag_end, current_tag))
        return tag_times

    def activity_to_tag(self, activity):
        keys = list(self.keyword_dict.keys())
        for key in keys:
            if not isinstance(activity, str) or activity.find(key) < 0:
                continue
            return self.keyword_dict[key]
        else:
            return 'other'

    def get_tagged_time(self, activities):
        tag_time = defaultdict(lambda: timedelta(0))
        for name, time_entries in activities.items():
            tag = self.activity_to_tag(name)
            tag_time[tag] += self.sum_time_entries(time_entries)
        return tag_time

    @staticmethod
    def sum_time_entries(time_entries):
        t = timedelta(0)
        for entry in time_entries:
            t += entry.total_time
        return t

    def timeline_stats(self, date):
        # acts = collect_all_activities()
        times = self.order_by_time(date)
        tag_times = self.times_to_tag_times(times)
        # tagged = get_tagged_time(acts)
        return times, tag_times


def sign(x):
    return -1 if x < 0 else +1


def _hours_minutes(secs):
    return int(secs / 3600), sign(secs) * ((abs(secs) % 3600) // 60)


def get_overtimes(tagged_time):
    target = Target()
    goal = target.sum_by_tag()
    for tag, sum_time in tagged_time.items():
        total_time = _hours_minutes(sum_time.seconds)
        if tag not in goal:
            yield tag, total_time, None, None
            continue

        target_seconds = goal[tag] * 3600
        target_time = _hours_minutes(target_seconds)
        overtime = _hours_minutes(sum_time.seconds - target_seconds)
        yield tag, total_time, target_time, overtime
