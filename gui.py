#!/usr/bin/env python3
import threading
import logging

from timenazi.activity import ActivityList
from timenazi.gui_frames import TimerGUI
from timenazi.tracker import window_listener

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    al = ActivityList()

    listener = threading.Thread(target=window_listener, args=(al,), daemon=True)
    listener.start()  # start thread

    with TimerGUI(al) as root:
        root.mainloop()

