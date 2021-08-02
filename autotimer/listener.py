import socket
import time


class PowerListener:
    """Listen for power on/off, lid open closed and suspend and wake up events."""

    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect("/var/run/acpid.socket")
        print("Connected to acpid")

    def read_events(self):
        events = self.sock.recv(4096)
        for event in events.decode('utf-8').split('\n'):
            event = event.split(' ')
            if len(event) < 2:
                continue
            # print(event)

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
            # elif event[0][:4] == "jack":
            #     if event[2] == 'unplug':
            #         return "Suspended"
            #     elif event[2] == 'plug':
            #         return "Woke up from suspension"
        return ""

    def suspended_or_lid_closed(self):
        message = self.read_events()
        if message in ['Suspended', 'Laptop lid closed']:
            print(message)
            return True
        return False

    def wait(self):
        """Wait until computer wakes up again or lid is opened."""
        while True:
            time.sleep(1)
            message = self.read_events()
            if message in ['Laptop lid opened', 'Plugged']:
                print(message)
                return


