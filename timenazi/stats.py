import logging
import re
from collections import defaultdict
from datetime import timedelta, datetime

from config import tag_to_keys, form
from .target import Target
from .activity import ActivityList


class TimerStats:

    def __init__(self):
        self.acts = dict()
        self.keyword_dict = self.get_keyword_dict()
        self._date = datetime.today()
        self.target = Target(self._date)

    @staticmethod
    def get_keyword_dict():
        inv_keys = dict()
        for tag, keywords in tag_to_keys.items():
            for key in keywords:
                inv_keys[key] = tag
        return inv_keys

    def activities_by_date(self, date_str):
        if date_str not in self.acts or date_str == datetime.today().strftime(form):
            # logging.info('Reading date: {}'.format(date_str))
            self.acts[date_str] = ActivityList(date=datetime.strptime(date_str, form))
        return self.acts[date_str].entries

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
        if len(times) > 0:
            tag_times.append((tag_start, tag_end, current_tag))
        return tag_times

    def timeline_stats(self, date_str):
        times = self.order_by_time(date_str)
        tag_times = self.times_to_tag_times(times)
        return times, tag_times

    def activity_to_tag(self, activity):
        keys = list(self.keyword_dict.keys())
        for key in keys:
            if not isinstance(activity, str) or re.search(key, activity, re.IGNORECASE) is None:
                continue
            return self.keyword_dict[key]
        else:
            return 'other'

    def time_per_tag(self, date_str):
        activities = self.activities_by_date(date_str)
        tpt = defaultdict(lambda: timedelta(0))
        for name, time_entries in activities.items():
            tag = self.activity_to_tag(name)
            tpt[tag] += self.sum_time_entries(time_entries)
        return tpt

    @staticmethod
    def sum_time_entries(time_entries):
        t = timedelta(0)
        for entry in time_entries:
            t += entry.total_time
        return t

    def get_overtimes(self):
        today = datetime.today()
        if today.day != self._date.day:
            self._date = today
            self.target.write()
            self.target = Target(today)

        date_str = self._date.strftime(form)
        logging.info("Loading data from {}".format(date_str))
        tpt = self.time_per_tag(date_str)
        self.target.update(date_str, tpt)

        tagged = self.target.sum_by_tag()
        for tag, (target_time, total_time) in tagged.items():
            total_time = total_time.total_seconds() / 3600.
            if tag not in tagged:
                yield tag, total_time, None
                continue
            if target_time is None:
                overtime = None
            else:
                overtime = total_time - target_time
            total_today = tpt[tag].total_seconds() / 3600.
            yield tag, total_today, overtime
