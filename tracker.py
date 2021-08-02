import time
import subprocess
import re
from datetime import datetime

from config import form, path
from autotimer.target import Target
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


if __name__ == "__main__":
    power = PowerListener()

    today = datetime.today().strftime(form)
    al = ActivityList(filename=path + 'log_' + today + '.json')

    old_window = get_active_window()
    start_time = datetime.now()
    try:
        while True:
            time.sleep(1)
            if power.suspended_or_lid_closed():
                al.end_activity(start_time, old_window)
                power.wait()  # wait until lid opened or wakes up
                old_window = new_window = get_active_window()
                start_time = datetime.now()
                print("Restart at: {}".format(start_time))

            new_window = get_active_window()
            if old_window == new_window:
                continue
            print(old_window)

            end_time = al.end_activity(start_time, old_window)
            start_time = end_time
            old_window = new_window
    except KeyboardInterrupt:
        al.write()
        Target().write()
