from __future__ import print_function
import time
from activity import *
import json
import datetime
import subprocess
import re


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


def get_active_window():
    """returns the details about the window not just the title"""
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m is not None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match is not None:
        return match.group("name").strip(b'"').decode('UTF-8')
    return None


if __name__ == '__main__':
    active_window_name = ""
    activity_name = ""
    start_time = datetime.datetime.now()
    filename = 'activities.json'
    acts = ActivityList()
    first_time = True

    try:
        while True:
            time.sleep(1)
            previous_site = ""
            new_window_name = get_active_window()
            # if 'Google Chrome' in new_window_name:
            #     new_window_name = l.get_chrome_url_x()

            if active_window_name == new_window_name:
                continue
            print(active_window_name)
            active_window_name = new_window_name

            if first_time:
                first_time = False
                continue
            first_time = False

            end_time = datetime.datetime.now()
            time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
            time_entry.get_specific_times()

            exists = False
            for activity in acts.activities:
                if activity.name == active_window_name:
                    exists = True
                    activity.time_entries.append(time_entry)

            if not exists:
                activity = Activity(active_window_name, [time_entry])
                acts.activities.append(activity)
            with open('activities.json', 'w') as json_file:
                json.dump(acts.serialize(), json_file, indent=4, sort_keys=True)
                start_time = datetime.datetime.now()

    except KeyboardInterrupt:
        with open('activities.json', 'w') as json_file:
            json.dump(acts.serialize(), json_file, indent=4, sort_keys=True)
