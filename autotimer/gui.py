import tkinter as tk
import datetime
from collections import namedtuple
from random import randint

from .stats import collect_all_activities, get_keyword_dict, get_tagged_time, order_by_time


Rectangle = namedtuple('Rectangle', 'x1 x2 activity color')


class Timeline:
    def __init__(self, x1, y1, x2, y2, times):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        span = 24 * 3600  # 1 day
        self.step = (x2 - x1) / float(span)
        self.rectangles = self.times_to_rectangles(times)

    @property
    def as_tuple(self):
        return self.x1, self.y1, self.x2, self.y2

    def time_to_x(self, t):
        return self.x1 + (t.hour * 3600 + t.minute * 60 + t.second) * self.step

    def x_to_time(self, x):
        seconds = int((x - self.x1) / self.step)
        hour = seconds // 3600
        seconds = seconds % 3600
        minute = seconds // 60
        seconds = seconds % 60
        return datetime.time(hour=hour, minute=minute, second=seconds).strftime('%H:%M:%S')

    def times_to_rectangles(self, times):
        entries = []
        colors = dict()
        for time in times:
            activity = time[2]
            r = 0, 255
            colors[activity] = colors.get(activity, (randint(*r), randint(*r), randint(*r)))
            rect = Rectangle(x1=self.time_to_x(time[0]),
                             x2=self.time_to_x(time[1]),
                             activity=activity,
                             color=colors[activity])
            entries.append(rect)
        return entries


class Canvas(tk.Canvas):
    def __init__(self, master, times):
        self.master = master
        super().__init__(master, width=1000, height=300)
        self.pack()
        self.timeline = Timeline(50, 50, 950, 100, times)
        self.create_rectangle(*self.timeline.as_tuple, outline="black")
        self.create_timeline()
        self.bind("<Motion>", self.moved)
        self.activity = self.create_text(10, 10, text="", anchor="nw")
        self.current_time = self.create_text(10, 30, text="", anchor="nw")

    def create_timeline(self):
        for rect in self.timeline.rectangles:
            col = "#%02x%02x%02x" % rect.color
            self.create_rectangle(rect.x1, self.timeline.y1 + 1, rect.x2, self.timeline.y2 - 1, fill=col, outline=col)

    def moved(self, event):
        time_text = ''
        if self.timeline.x1 <= event.x <= self.timeline.x2 and self.timeline.y1 <= event.y <= self.timeline.y2:
            time_text = self.timeline.x_to_time(event.x)
        self.itemconfigure(self.current_time, text=time_text)

        for rect in self.timeline.rectangles:
            if rect.x1 <= event.x <= rect.x2 and self.timeline.y1 <= event.y <= self.timeline.y2:
                self.itemconfigure(self.activity, text=rect.activity)
                return
        self.itemconfigure(self.activity, text='Untracked')


class TimerGUI(tk.Tk):
    def __init__(self, times):
        super().__init__()
        self.geometry("1000x300")
        self.title('Statistics and stuff')
        self._frame = Canvas(self, times)


def get_times():
    acts = collect_all_activities()
    times = order_by_time(acts, date=None)
    return times
    # key_dict = get_keyword_dict()
    # tagged = get_tagged_time(acts, key_dict)
    # print_overtime(tagged)
