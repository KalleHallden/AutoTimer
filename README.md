To the best of my knowledge, this is the ONLY automatic time tracker for 
Linux  that supports **automatic** tracking and grouping of activities such as "Programming", 
"Book writing", "Leisure" etc. (also known as **autotagging**).

![gui_screenshot](https://user-images.githubusercontent.com/88085405/129172414-a76a2b32-14de-457a-9f8f-0464a39b5816.png)

This application notices when a window is active, i.e. where the current focus is 
and the real time spent in that window (=activity) is tracked. It is visualized on a timeline
(similar to ManicTime), where each activity is marked by a different color. The
second timeline tracks the tags (=groups of activities), which are recognized by 
keywords. For example, if the window name contains "python" as substring, it is 
tagged as "Programming".

Goals can be set for each tag, for example 4 hours every work day for "Programming" 
and 1 hour for "Book writing". Holidays can be set for a timeout. Overtime is computed for each tag,
for example, if 4 hours is planning per day for "Programming" but after 3 days 
only 10 hours have been spent doing so, the overtime will show -2 hours.

To get started, configure config.py: 
- path for logging tracked data
- the first date for logging
- <tag_to_keys> maps tags to keywords
- set workday and holiday target times, e.g. how many hours you want to spend "Programming" or "Reading" etc. 
- `python3 tracker.py` runs the tracker in the background
- start the GUI with ./gui.py

Dependencies:
- python-dateutil

