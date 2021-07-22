import time
import datetime
import subprocess
import re

from activity import *


def get_active_window():
    """Return the details about the window not just the title."""
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


if __name__ == "__main__":
    active_window = get_active_window()
    start_time = datetime.datetime.now()
    filename = 'activities.json'
    acts = ActivityList()

    try:
        while True:
            time.sleep(1)

            new_window = get_active_window()
            if active_window == new_window:
                continue
            print(active_window)
            active_window = new_window

            end_time = datetime.datetime.now()
            time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0, specific=True)

            activity = acts.by_name(active_window)
            if activity:
                activity.time_entries.append(time_entry)
            else:
                acts.activities.append(Activity(active_window, [time_entry]))

            acts.write(filename)
            start_time = datetime.datetime.now()

    except KeyboardInterrupt:
        acts.write(filename)
