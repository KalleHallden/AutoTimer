import os
from collections import defaultdict
from datetime import timedelta, datetime

from config import path, tag_to_keys, form
from .target import Target
from .activity import ActivityList


def logged_dates():
    data = []
    for files in os.listdir(path):
        filename = os.path.join(path, files)
        if not os.path.isfile(filename) or files[:4] != 'log_':
            continue
        data.append((filename, files[4:-5]))
    return sorted(data, key=lambda i: i[1])


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

    def activities_by_date(self, date_str):
        if date_str not in self.acts or date_str == datetime.today().strftime(form):
            print('Reading date: {}'.format(date_str))
            self.acts[date_str] = ActivityList(filename=path + 'log_' + date_str + '.json')
        return self.acts[date_str].acts

    def order_by_time(self, date_str):
        times = []
        activities = self.activities_by_date(date_str)
        for name, time_entries in activities.items():
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

    def get_tagged_time(self):
        tag_time = defaultdict(lambda: timedelta(0))
        for _, date_str in logged_dates():
            activities = self.activities_by_date(date_str)
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
        times = self.order_by_time(date)
        tag_times = self.times_to_tag_times(times)
        return times, tag_times

    def get_overtimes(self):
        tagged_time = self.get_tagged_time()
        target = Target()
        goal = target.sum_by_tag()
        for tag, total_time in tagged_time.items():
            if tag not in goal:
                yield tag, total_time, None
                continue

            target_time = timedelta(hours=goal[tag])
            yield tag, total_time, target_time
