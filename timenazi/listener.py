import logging
import socket
import time


class PowerListener:
    """Listen for power on/off, lid open closed and suspend and wake up events."""

    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect("/var/run/acpid.socket")
        logging.info("Connected to acpid")

    def read_events(self):
        events = self.sock.recv(4096)
        for event in events.decode('utf-8').split('\n'):
            event = event.split(' ')
            if len(event) < 2:
                continue

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
        return ""

    def lid_closed(self):
        message = self.read_events()
        if message == 'Laptop lid closed':
            logging.info("\n*** {} ***\n".format(message))
            return True
        return False

    def wait(self):
        """Wait until computer wakes up again or lid is opened."""
        while True:
            time.sleep(1)
            message = self.read_events()
            if message == 'Laptop lid opened':
                logging.info("\n*** {} ***\n".format(message))
                return


