#!/usr/bin/env python3
import threading

from timenazi.activity import ActivityList
from timenazi.gui_frames import TimerGUI
from timenazi.tracker import window_listener

al = ActivityList()

listener = threading.Thread(target=window_listener, args=(al,), daemon=True)
listener.start()  # start thread

with TimerGUI(al) as root:
    root.mainloop()

