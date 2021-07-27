import os
from collections import defaultdict
from datetime import datetime, timedelta

from activity import ActivityList

path = 'log/'
start_date = datetime.strptime('2021-07-27', '%Y-%m-%d')

# keywords for each tag
tag_to_keys = {
    'Programming': ['william', 'ai/', 'IPython', 'Source.gv', 'Stack Overflow', 'python', 'Python'],
    'AGI book': ['book.lyx', 'Inkscape'],
}
# target time in hours
goal = {
    'Programming': 4,
    'AGI book': 1,
}


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


def get_keyword_dict():
    inv_keys = dict()
    for tag, keywords in tag_to_keys.items():
        for key in keywords:
            inv_keys[key] = tag
    return inv_keys


def get_tagged_time(activities, keyword_dict):
    keys = list(keyword_dict.keys())
    tag_time = defaultdict(lambda: timedelta(0))
    for name, time_entries in activities.items():
        for key in keys:
            if not isinstance(name, str) or name.find(key) < 0:
                continue
            tag = keyword_dict[key]
            tag_time[tag] += sum_time_entries(time_entries)
            break
        else:
            tag_time['other'] += sum_time_entries(time_entries)
    return tag_time


def sum_time_entries(time_entries):
    t = timedelta(0)
    for entry in time_entries:
        t += entry.total_time
    return t


def _hours_minutes(secs):
    return secs // 3600, (secs % 3600) // 60


def print_overtime(tagged_time):
    today = datetime.today()
    days_since_start = (today - start_date).days + 1
    for tag, sum_time in tagged_time.items():
        print("\nActivity: {}".format(tag))
        total_time = _hours_minutes(sum_time.seconds)
        print("Total time:  {} hours, {} minutes".format(*total_time))
        if tag not in goal:
            continue

        target_seconds = days_since_start * goal[tag] * 3600
        target_time = _hours_minutes(target_seconds)
        overtime = _hours_minutes(sum_time.seconds - target_seconds)
        print("Target time: {} hours {} minutes".format(*target_time))
        print("Overtime:    {} hours {} minutes".format(*overtime))


if __name__ == "__main__":
    acts = collect_all_activities()
    key_dict = get_keyword_dict()
    tagged = get_tagged_time(acts, key_dict)
    print_overtime(tagged)

