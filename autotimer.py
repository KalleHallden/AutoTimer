import time
import subprocess
import re
# import socket
from datetime import datetime

from config import form, path
from autotimer.target import Target
from autotimer.activity import *
# from autotimer.listener import read_events


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
    old_window = get_active_window()
    start_time = datetime.now()

    today = datetime.today().strftime(form)
    filename = path + 'log_' + today + '.json'
    al = ActivityList(filename=filename)

    # s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # s.connect("/var/run/acpid.socket")
    # print("Connected to acpid")

    try:
        while True:
            time.sleep(1)
            # message = read_events(s.recv(4096))
            # if message:
            #     print(message)

            new_window = get_active_window()
            if old_window == new_window:
                continue
            print(old_window)

            end_time = datetime.now()
            time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0, specific=True)
            al.acts[old_window].append(time_entry)
            al.write(filename)
            start_time = end_time
            old_window = new_window

    except KeyboardInterrupt:
        al.write(filename)
        Target().write()
