import gi
import time
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck, Gtk


if __name__ == '__main__':
    screen = Wnck.Screen.get_default()
    screen.force_update()
    while True:
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(0.5)
        w = screen.get_active_window()
        print(w.get_name())
