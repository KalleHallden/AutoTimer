import json
import lz4.block
import pathlib
from time import time

# Set up path and regex for files
path = pathlib.Path.home().joinpath('.mozilla/firefox')
files = path.glob('*default*release*/sessionstore-backups/recovery.jsonlz4')
# files = path.glob('5ov6afhq.default-release-1/sessionstore-backups/recovery'+
#                   '.jsonlz4')

for f in files:
    # decompress if necessary
    b = f.read_bytes()
    if b[:8] == b'mozLz40\0':
        b = lz4.block.decompress(b[8:])

    # load as json
    j = json.loads(b)
    if 'windows' in j.keys():
        for w in j['windows']:

            # Variables for keeping track of most recent tab
            most_recent_tab_index = ''
            min_time = 1000

            # run through tabs
            for t in w['tabs']:
                # Firefox does not 0-index
                i = t['index'] - 1

                # Convert time to seconds
                access_time = int((int(time()*1000) - t['lastAccessed'])/600)

                if access_time < min_time:
                    most_recent_tab_index = t['entries'][i]['url']

            print("MOST RECENT TAB: ", most_recent_tab_index)
