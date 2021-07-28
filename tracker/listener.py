def read_events(events):
    for event in events.decode('utf-8').split('\n'):
        event = event.split(' ')
        if len(event) < 2:
            continue
        print(event)

        if event[0] == 'ac_adapter':
            if event[3] == '00000001':
                return "Plugged"
            else:
                return "Unplugged"
        elif event[0] == 'button/power':
            return "Power button pressed"
        elif event[0] == 'button/lid':
            if event[2] == 'open':
                return "Laptop lid opened"
            elif event[2] == 'close':
                return "Laptop lid closed"
        elif event[0] == "jack/lineout":
            if event[2] == 'unplug':
                return "Suspended"
            elif event[2] == 'plug':
                return "Woke up from suspension"
    return ""

