import tkinter as tk
from random import randint

from .stats import collect_all_activities, get_keyword_dict, get_tagged_time, order_by_time


class Canvas(tk.Canvas):
    def __init__(self, master, times):
        self.master = master
        super().__init__(master, width=1000, height=150)
        self.pack()
        self.coordinates = self.times_to_coordinates(times)
        self.create_timeline()
        self.bind("<Motion>", self.moved)
        self.tag = self.create_text(10, 10, text="", anchor="nw")

    @staticmethod
    def times_to_coordinates(times):
        x0, x1 = 0, 1000
        total_seconds = 24 * 3600  # 1 day
        step = (x1 - x0) / float(total_seconds)
        coordinates = []
        for time in times:
            start = x0 + (time[0].hour * 3600 + time[0].minute * 60 + time[0].second) * step
            end = x0 + (time[1].hour * 3600 + time[1].minute * 60 + time[1].second) * step
            coordinates.append((start, end, time[2]))
        return coordinates

    def create_timeline(self):
        for interval in self.coordinates:
            rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.create_rectangle(interval[0], 50, interval[1], 100, fill="#%02x%02x%02x" % rgb)

    def moved(self, event):
        y1, y2 = 50, 100
        for interval in self.coordinates:
            if interval[0] <= event.x <= interval[1] and y1 <= event.y <= y2:
                self.itemconfigure(self.tag, text=interval[2])
                return
        self.itemconfigure(self.tag, text='')


class TimerGUI(tk.Tk):
    def __init__(self, times):
        super().__init__()
        self.geometry("1000x150")
        self.title('Statistics and stuff')
        # acts, times = self.get_data()
        self._frame = Canvas(self, times)


def get_data():
    acts = collect_all_activities()
    times = order_by_time(acts, date=None)
    return acts, times
    # key_dict = get_keyword_dict()
    # tagged = get_tagged_time(acts, key_dict)
    # print_overtime(tagged)
