from AppKit import NSWorkspace
import time

active_window_name = ""
while True:

    new_window_name = (NSWorkspace.sharedWorkspace()
    .activeApplication()['NSApplicationName'])
    
    if active_window_name != new_window_name:
        active_window_name = new_window_name
        print(active_window_name)
    
    time.sleep(10)

