import time
import subprocess
import re
from datetime import datetime

from autotimer.activity import ActivityList
from autotimer.listener import PowerListener


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
        return match.group("name").strip(b'"').decode('UTF-8').replace('*', '')
    return None


def restart(current_time):
    w = get_active_window()
    print("Restart at: {}\n".format(current_time))
    return w, w, current_time


if __name__ == "__main__":
    power = PowerListener()

    al = ActivityList()

    old_window = get_active_window()
    start_time = last_record = datetime.now()
    try:
        while True:
            time.sleep(1)
            now = datetime.now()

            # computer was likely suspended
            if (now - last_record).total_seconds() > 5:
                print("\n*** waking up from suspension ***\n")
                al.end_activity(old_window, start_time, last_record)
                old_window, new_window, start_time = restart(now)

            # laptop lid closed
            if power.lid_closed():
                al.end_activity(old_window, start_time, now)
                power.wait()  # wait until lid opened or wakes up
                now = datetime.now()
                old_window, new_window, start_time = restart(now)

            last_record = now
            new_window = get_active_window()
            if old_window == new_window:
                continue
            al.end_activity(old_window, start_time, now)
            start_time = now
            old_window = new_window
    except KeyboardInterrupt:
        al.write()
