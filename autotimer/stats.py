import os
from collections import defaultdict
from datetime import timedelta, datetime

from config import path, tag_to_keys
from .target import Target
from .activity import ActivityList


def collect_all_activities():
    """Collect activities from every day."""
    activities = defaultdict(list)
    for files in os.listdir(path):
        filename = os.path.join(path, files)
        if not os.path.isfile(filename):
            continue
        print('Reading: {}'.format(filename))
        al = ActivityList(filename=filename)
        al.append(activities)
    return activities


def order_by_time(activities, date=None):
    date = date or datetime.today()
    times = []
    for name, time_entries in activities.items():
        for entry in time_entries:
            s = entry.start_time
            if s.day != date.day or s.month != date.month or s.year != date.year:
                continue
            times.append((s, entry.end_time, name))
    return sorted(times, key=lambda x: x[0])


def times_to_tag_times(times, keyword_dict):
    """Group activities and their sorted times into times for tags."""
    tag_times = []
    current_tag = ""
    tag_start, tag_end = None, None
    for start, end, activity in times:
        tag = activity_to_tag(activity, keyword_dict)
        # if tag changes or distance between equal tags is more than 5 seconds, make new tag entry
        if tag != current_tag or tag_end and (start - tag_end).seconds > 30:
            if current_tag != "":
                tag_times.append((tag_start, tag_end, current_tag))
            current_tag = tag
            tag_start = start
        tag_end = end
    tag_times.append((tag_start, tag_end, current_tag))
    return tag_times


def get_keyword_dict():
    inv_keys = dict()
    for tag, keywords in tag_to_keys.items():
        for key in keywords:
            inv_keys[key] = tag
    return inv_keys


def activity_to_tag(activity, keyword_dict):
    keys = list(keyword_dict.keys())
    for key in keys:
        if not isinstance(activity, str) or activity.find(key) < 0:
            continue
        return keyword_dict[key]
    else:
        return 'other'


def get_tagged_time(activities, keyword_dict):
    tag_time = defaultdict(lambda: timedelta(0))
    for name, time_entries in activities.items():
        tag = activity_to_tag(name, keyword_dict)
        tag_time[tag] += sum_time_entries(time_entries)
    return tag_time


def sum_time_entries(time_entries):
    t = timedelta(0)
    for entry in time_entries:
        t += entry.total_time
    return t


def sign(x):
    return -1 if x < 0 else +1


def _hours_minutes(secs):
    return int(secs / 3600), sign(secs) * ((abs(secs) % 3600) // 60)


def get_overtimes(tagged_time):
    target = Target()
    goal = target.sum_by_tag()
    for tag, sum_time in tagged_time.items():
        # print("\nActivity: {}".format(tag))
        total_time = _hours_minutes(sum_time.seconds)
        # print("Total time:  {} hours, {} minutes".format(*total_time))
        if tag not in goal:
            yield tag, total_time, None, None
            continue

        target_seconds = goal[tag] * 3600
        target_time = _hours_minutes(target_seconds)
        overtime = _hours_minutes(sum_time.seconds - target_seconds)
        yield tag, total_time, target_time, overtime
        # print("Target time: {} hours {} minutes".format(*target_time))
        # print("Overtime:    {} hours {} minutes".format(*overtime))


def get_stats():
    acts = collect_all_activities()
    times = order_by_time(acts, date=None)
    key_dict = get_keyword_dict()
    tag_times = times_to_tag_times(times, key_dict)
    tagged = get_tagged_time(acts, key_dict)
    return times, tag_times, tagged
