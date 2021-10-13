import logging
import tkinter as tk

from texttable import Texttable
from tkcalendar import Calendar
from datetime import datetime
from collections import namedtuple
from hashlib import sha256

from config import form, path, tag_to_keys
from .activity import TimeEntry
from .stats import TimerStats

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

    def is_inside(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def time_to_x(self, t):
        return self.x1 + (t.hour * 3600 + t.minute * 60 + t.second) * self.step

    def x_to_time(self, x, date=None):
        seconds = int((x - self.x1) / self.step)
        hour = seconds // 3600
        seconds = seconds % 3600
        minute = seconds // 60
        seconds = seconds % 60
        y, m, d = (date.year, date.month, date.day) if date else (2021, 1, 1)
        return datetime(year=y, month=m, day=d, hour=hour, minute=minute, second=seconds)

    @staticmethod
    def string_to_color(name):
        bytes_name = bytes('#q' + str(name), 'utf-8')
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
        self.width = 1000
        super().__init__(master, width=self.width, height=270, bg='white', bd=0, highlightthickness=0)

        self.bind("<Motion>", self.moved)

        self.act_text, self.tag_text, self.current_time = None, None, None
        self.act_timeline = self.tag_timeline = None
        self.active_date = datetime.today().strftime(form)
        self.load(self.active_date)

        # self.bind("<Button-1>", lambda x: print("LEFT CLICK"))
        # self.bind("<Double-Button-1>", lambda x: print("DOUBLE CLICK"))
        # def drag_handler(event):
        #     print(event.x, event.y)
        self._drag_rect = None
        self._drag_start = None
        self.bind("<ButtonPress-1>", self._start_drag)
        self.bind("<B1-Motion>", self._on_move_press)
        self.bind("<ButtonRelease-1>", self._end_drag)

    def load(self, date_str):
        self.active_date = date_str
        self.delete('all')
        self.act_text = self.create_text(10, 200, text="", anchor="nw")
        self.tag_text = self.create_text(10, 220, text="", anchor="nw")
        self.current_time = self.create_text(10, 240, text="", anchor="nw")

        act_times, tag_times = self.master.timer_stats.timeline_stats(date_str)
        self.act_timeline = Timeline(10, 30, self.width - 10, 80, act_times)
        self.tag_timeline = Timeline(10, 100, self.width - 10, 150, tag_times)
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
            time_text = self.act_timeline.x_to_time(event.x).strftime('%H:%M:%S')
        self.itemconfigure(self.current_time, text=time_text)

        self.move_check(event, self.act_timeline, self.act_text, ys)
        self.move_check(event, self.tag_timeline, self.tag_text, ys)

    def move_check(self, event, timeline, text_label, ys):
        for rect in timeline.rectangles:
            if rect.x1 <= event.x < rect.x2 and (ys[0][0] <= event.y <= ys[0][1] or ys[1][0] <= event.y <= ys[1][1]):
                self.itemconfigure(text_label, text=rect.activity)
                return
        self.itemconfigure(text_label, text='')

    def _start_drag(self, event):
        if not self.act_timeline.is_inside(event.x, event.y):
            return
        self._drag_start = (event.x, event.y)

    def _on_move_press(self, event):
        if self._drag_start is None:
            return
        if not self.act_timeline.is_inside(event.x, event.y):
            return
        if self._drag_rect is not None:
            self.delete(self._drag_rect)
        drag_end = (event.x, event.y)
        self._drag_rect = self.create_rectangle(self._drag_start[0], self.act_timeline.y1+1,
                                                drag_end[0], self.act_timeline.y2-1, fill="", outline="#aaaaaa")

    def _end_drag(self, event):
        if not self.act_timeline.is_inside(event.x, event.y):
            self._drag_start = None
            return
        self._add_activity(self._drag_start[0], event.x)
        self.delete(self._drag_rect)
        self._drag_start = None

    def _add_activity(self, x0, x1):
        date = datetime.strptime(self.active_date, form)
        t0 = self.act_timeline.x_to_time(x0, date=date)
        t1 = self.act_timeline.x_to_time(x1, date=date)
        time_entry = TimeEntry(t0, t1, 0, 0, 0, 0, specific=True)
        activity, tag = ActivityWindow(self.master).get_info()
        if activity == '':
            return
        al = self.master.timer_stats.acts[self.active_date]
        al.entries[activity].append(time_entry)
        al.write()
        if self.active_date == self.master.current_al.date.strftime(form):
            logging.info('Updating current activity list..')
            self.master.current_al.entries[activity].append(time_entry)
        logging.info(activity, tag)
        self.load(self.active_date)
        self.master.overtime_box()


class ActivityWindow:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        lab = tk.Label(self.window, text="Enter activity:")
        lab.grid(column=0, row=0, sticky='w', padx=5)

        self.act_var = tk.StringVar()
        self.text = tk.Entry(self.window, textvariable=self.act_var)
        self.text.grid(column=0, row=1, columnspan=2, padx=5)
        self.text.focus()

        tag_lab = tk.Label(self.window, text="Assign tag:")
        tag_lab.grid(column=0, row=2, sticky='w', padx=5)

        self.tag_sel = tk.StringVar()
        self.tag_sel.set('Other')
        tags = list(tag_to_keys.keys())
        for k, tag in enumerate(tags):
            r = tk.Radiobutton(self.window, text=tag, value=tag, variable=self.tag_sel)
            r.grid(column=0, row=3+k, sticky='w', padx=5)

        cancel_button = tk.Button(self.window, text='Cancel', command=self.cancel)
        cancel_button.grid(column=0, row=3 + len(tags), sticky='sw', pady=10)

        add_button = tk.Button(self.window, text='Add', command=self.window.destroy)
        add_button.grid(column=1, row=3 + len(tags), sticky='se', pady=10)

    def get_info(self):
        self.window.deiconify()
        self.window.wait_window()
        activity_name = self.act_var.get()
        tag = self.tag_sel.get()
        return activity_name, tag

    def cancel(self):
        self.act_var.set('')
        self.tag_sel.set('')
        self.window.destroy()


class TimerGUI(tk.Tk):
    def __init__(self, current_al):
        super().__init__()
        self.title('TimeNazi')
        self.configure(bg='white')

        self.set_icon()

        self.current_al = current_al
        self.timer_stats = TimerStats()
        self.date_selector()

        self._frame = Canvas(self)
        self._frame.grid(column=0, row=2, columnspan=5, sticky='s')

        self.overtime_box()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("Finalizing..")
        if self.timer_stats:
            self.timer_stats.target.write()
        self.current_al.write()

    def set_icon(self):
        icon = tk.PhotoImage(file=path + "icon.png")
        self.iconphoto(False, icon)

    def date_selector(self):
        t = datetime.today()
        cal = Calendar(self, selectmode="day", year=t.year, month=t.month, day=t.day)
        cal.grid(column=0, row=0, padx=10, pady=10, sticky='s')

        # Define Function to select the date
        def get_date():
            date_str = datetime.strptime(cal.get_date(), '%m/%d/%y').strftime(form)
            self._frame.load(date_str)
            self.overtime_box()

        # Create a button to pick the date from the calendar
        button = tk.Button(text="Show tracked time", command=get_date)
        button.grid(column=0, row=1, sticky='n')

    def overtime_box(self):
        text = tk.Text(self, width=30, height=1, highlightthickness=0, bd=0)
        text.insert('1.0', self.overtime())
        text['state'] = 'disabled'
        text.grid(column=1, row=0, rowspan=2, padx=0, pady=10, sticky='nsew')

    def overtime(self):
        table = Texttable()
        table.set_cols_dtype(['t', 'f', 'f'])
        table.set_cols_align(["r", "l", "l"])
        table.add_row(["Tag", "spent", "overtime"])
        for tag, spent_today, overtime in self.timer_stats.get_overtimes():
            if tag == "other":
                continue
            table.add_row([tag, spent_today, "" if overtime is None else overtime])
        return table.draw()
