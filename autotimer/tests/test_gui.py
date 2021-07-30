from datetime import datetime, timedelta

from ..gui import TimerGUI, get_times


def dummy_times():
    t0 = datetime(year=2021, month=7, day=27, hour=9)
    duration = timedelta(hours=1)
    times = [(t0, t0 + duration, 'activity 0')]
    for n in range(5):
        t0 += duration + timedelta(minutes=20)
        times.append((t0, t0 + duration, 'activity {}'.format(n + 1)))
    return times


def test_hovering():
    times = get_times()
    root = TimerGUI(times)
    root.mainloop()
