import tkinter as tk
import datetime
from collections import namedtuple
from random import randint

from .stats import collect_all_activities, get_keyword_dict, get_tagged_time, order_by_time, times_to_tag_times, \
    get_overtimes

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
        super().__init__(master, width=1000, height=700)
        self.pack()

        act_times, tag_times, tagged = times
        self.act_timeline = Timeline(50, 100, 950, 150, act_times)
        self.create_timeline(self.act_timeline)

        self.tag_timeline = Timeline(50, 170, 950, 220, tag_times)
        self.create_timeline(self.tag_timeline)

        self.bind("<Motion>", self.moved)
        self.act_text = self.create_text(10, 10, text="", anchor="nw")
        self.tag_text = self.create_text(10, 30, text="", anchor="nw")
        self.current_time = self.create_text(10, 50, text="", anchor="nw")

        self.overtime(tagged)

    def create_timeline(self, timeline):
        self.create_rectangle(*timeline.as_tuple, outline="black")
        for rect in timeline.rectangles:
            col = "#%02x%02x%02x" % rect.color
            self.create_rectangle(rect.x1, timeline.y1 + 1, rect.x2, timeline.y2 - 1, fill=col, outline=col)

    def moved(self, event):
        time_text = ''
        ys = [(self.act_timeline.y1, self.act_timeline.y2), (self.tag_timeline.y1, self.tag_timeline.y2)]
        if self.act_timeline.x1 <= event.x < self.act_timeline.x2 and \
                (ys[0][0] <= event.y <= ys[0][1] or ys[1][0] <= event.y <= ys[1][1]):
            time_text = self.act_timeline.x_to_time(event.x)
        self.itemconfigure(self.current_time, text=time_text)

        self.move_check(event, self.act_timeline, self.act_text, ys)
        self.move_check(event, self.tag_timeline, self.tag_text, ys)

    def move_check(self, event, timeline, text_label, ys):
        for rect in timeline.rectangles:
            if rect.x1 <= event.x < rect.x2 and (ys[0][0] <= event.y <= ys[0][1] or ys[1][0] <= event.y <= ys[1][1]):
                self.itemconfigure(text_label, text=rect.activity)
                return
        if timeline.x1 <= event.x < timeline.x2 and (ys[0][0] <= event.y <= ys[0][1] or ys[1][0] <= event.y <= ys[1][1]):
            self.itemconfigure(text_label, text='Untracked')
        else:
            self.itemconfigure(text_label, text='')

    def overtime(self, tagged):
        y = 250
        for k, (tag, total_time, target_time, overtime) in enumerate(get_overtimes(tagged)):
            self.create_text(10, y, text="Activity: {}".format(tag), anchor="nw")
            self.create_text(10, y + 20, text="Total time:  {} hours, {} minutes".format(*total_time), anchor="nw")
            if target_time is None:
                y += 60
                continue
            self.create_text(10, y + 40, text="Target time: {} hours {} minutes".format(*target_time), anchor="nw")
            self.create_text(10, y + 60, text="Overtime:    {} hours {} minutes".format(*overtime), anchor="nw")
            y += 100


class TimerGUI(tk.Tk):
    def __init__(self, times):
        super().__init__()
        self.geometry("1000x700")
        self.title('Statistics and stuff')
        self._frame = Canvas(self, times)
