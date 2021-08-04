import tkinter as tk

from tkinter import ttk
from datetime import time, datetime, timedelta
from collections import namedtuple
from hashlib import sha256

from config import form
from .stats import TimerStats, logged_dates

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
        return time(hour=hour, minute=minute, second=seconds).strftime('%H:%M:%S')

    @staticmethod
    def string_to_color(name):
        bytes_name = bytes(str(name), 'utf-8')
        hex_hash = sha256(bytes_name).hexdigest()
        return '#' + hex_hash[:6]

    def times_to_rectangles(self, times):
        entries = []
        colors = dict()

        for t in times:
            activity = t[2]
            colors[activity] = colors.get(activity, self.string_to_color(activity))
            rect = Rectangle(x1=self.time_to_x(t[0]),
                             x2=self.time_to_x(t[1]),
                             activity=activity,
                             color=colors[activity])
            entries.append(rect)
        return entries


class Canvas(tk.Canvas):
    def __init__(self, master):
        self.master = master
        super().__init__(master, width=1000, height=270)

        self.bind("<Motion>", self.moved)

        self.act_text, self.tag_text, self.current_time = None, None, None
        self.act_timeline = self.tag_timeline = None
        today = datetime.today().strftime(form)
        self.load(today)

    def load(self, date_str):
        self.delete('all')
        self.act_text = self.create_text(10, 30, text="", anchor="nw")
        self.tag_text = self.create_text(10, 50, text="", anchor="nw")
        self.current_time = self.create_text(10, 70, text="", anchor="nw")

        act_times, tag_times = self.master.timer_stats.timeline_stats(date_str)
        self.act_timeline = Timeline(10, 100, 990, 150, act_times)
        self.tag_timeline = Timeline(10, 170, 990, 220, tag_times)
        self.create_timeline(self.act_timeline, ticks=False)
        self.create_timeline(self.tag_timeline, ticks=True)

    def create_timeline(self, timeline, ticks=False):
        self.create_rectangle(*timeline.as_tuple, outline="black")
        for rect in timeline.rectangles:
            self.create_rectangle(rect.x1, timeline.y1 + 1, rect.x2, timeline.y2 - 1, fill=rect.color, outline=rect.color)
        if not ticks:
            return
        for n in range(25):
            x = timeline.x1 + n * (timeline.x2 - timeline.x1) / 24
            self.create_line(x, timeline.y2, x, timeline.y2 + 4)
            self.create_text(x - 5, timeline.y2 + 6, font=('Arial', 8), text=str(n).zfill(2), anchor="nw")

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
        self.itemconfigure(text_label, text='')


class TimerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1020x600")
        self.title('Autotimer statistics')

        self.timer_stats = TimerStats()
        self.day_sel = None
        self.day_selector()

        self._frame = Canvas(self)
        self._frame.grid(column=0, row=3)

        self.listbox = self.scrollbar = None
        self.overtime_listbox()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timer_stats.target.write()

    def day_selector(self):
        label = ttk.Label(text="Select a day:")
        label.grid(column=0, row=0, sticky='w')

        # create a combobox
        selected_day = tk.StringVar()

        self.day_sel = ttk.Combobox(self, textvariable=selected_day)
        self.day_sel['values'] = sorted([day for _, day in logged_dates()])[::-1]
        self.day_sel['state'] = 'readonly'  # normal
        self.day_sel.grid(column=0, row=1, sticky='w')

        self.day_sel.bind('<<ComboboxSelected>>', self.day_changed)

    def day_changed(self, event):
        self._frame.load(self.day_sel.get())
        self.overtime_listbox()

    def overtime_listbox(self):
        text = tk.StringVar(value=self.overtime())

        self.listbox = tk.Listbox(self, listvariable=text, height=15, selectmode='extended')
        self.listbox.grid(column=0, row=4, sticky='nwes')

        # link a scrollbar to a list
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.grid(column=1, row=4, sticky='ns')

    def overtime(self):
        text = []
        for k, (tag, total_time, target_time) in enumerate(self.timer_stats.get_overtimes()):
            if tag == "other":
                continue
            text.append("Activity: {}".format(tag))
            text.append("Total time:  {}".format(total_time))
            if target_time is None:
                text.append("")
                continue
            text.append("Target time: {}".format(target_time))
            overtime = total_time - target_time
            s = str(overtime) if overtime >= timedelta(0) else '- ' + str(target_time - total_time)
            text.append("Overtime:    {}".format(s))
            text.append("")
        return text


def run():
    with TimerGUI() as root:
        root.mainloop()
