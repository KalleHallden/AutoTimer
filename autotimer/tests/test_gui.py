from datetime import datetime, timedelta

from ..gui import TimerGUI


def test_hovering():
    t0 = datetime(year=2021, month=7, day=27, hour=9)
    duration = timedelta(hours=1)
    times = [(t0, t0 + duration, 'task 0')]
    for n in range(5):
        t0 += duration + timedelta(minutes=20)
        times.append((t0, t0 + duration, 'task {}'.format(n + 1)))

    root = TimerGUI(times)
    root.mainloop()
