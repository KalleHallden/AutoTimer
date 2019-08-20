from __future__ import print_function
from AppKit import NSWorkspace
import time
from Foundation import *
from os import system
from activity import *
import json
import datetime

active_window_name = ""
activity_name = ""
start_time = datetime.datetime.now()
activeList = AcitivyList([]) 
first_time = True
try:
    activeList.initialize_me()
except Exception:
    print('No json')

try:
    while True:
        new_window_name = (NSWorkspace.sharedWorkspace()
        .activeApplication()['NSApplicationName'])
        if active_window_name != new_window_name:
            active_window_name = new_window_name
            print(active_window_name)
            if active_window_name == 'Google Chrome':
                textOfMyScript = """tell app "google chrome" to get the url of the active tab of window 1"""
                s = NSAppleScript.initWithSource_(NSAppleScript.alloc(), textOfMyScript)
                results, err = s.executeAndReturnError_(None)
                print(results.stringValue())
                activity_name = results.stringValue()
            else:
                activity_name = active_window_name
            
            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()
            
                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)
            
                if not exists:
                    activity = Activity(activity_name, [time_entry])
                    activeList.activities.append(activity)  
                with open('activities.json', 'w') as json_file:  
                    json.dump(activeList.serialize(), json_file)
            first_time = False
        time.sleep(10)
except KeyboardInterrupt:
    with open('activities.json', 'w') as json_file:  
        json.dump(activeList.serialize(), json_file)
