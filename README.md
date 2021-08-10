Tracking the desktop applications in real time and time spent on each application. Autotagging supported.

Initially based on this https://youtu.be/ZBLYcvPl1MA 

Dependencies:
- python-dateutil

Configure config.py to set 
- path for logging tracked data
- the first date for logging
- <tag_to_keys> maps tags to keywords, i.e. if window name contains a substring "python" then this activity is grouped under the tag "Programming"
- set workday and holiday target times, e.g. how many hours you want to spend "Programming" or "Reading" etc.
