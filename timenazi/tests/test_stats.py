from datetime import datetime, timedelta

from ..stats import TimerStats


def dummy_times():
    t0 = datetime(year=2021, month=7, day=27, hour=9)
    duration = timedelta(hours=1)
    times = [(t0, t0 + duration, 'activity 0')]
    for n in range(5):
        t0 += duration + timedelta(minutes=20) if n % 2 == 1 else duration + timedelta(seconds=3)
        times.append((t0, t0 + duration, 'activity {}'.format(n + 1)))
    return times


def test_times_to_tag_times():
    stats = TimerStats()
    times = dummy_times()
    stats.keyword_dict = {'activity 0': 'work', 'activity 1': 'work', 'activity 2': 'work', 'activity 3': 'fun',
                          'activity 4': 'fun', 'activity 5': 'work'}
    tag_times = stats.times_to_tag_times(times)
    tt = [(start.strftime("%H:%M:%S"), end.strftime("%H:%M:%S"), tag) for start, end, tag in tag_times]
    # note that the first two entries have been grouped to one
    assert tt == [('09:00:00', '11:00:03', 'work'), ('11:20:03', '12:20:03', 'work'), ('12:20:06', '13:20:06', 'fun'),
                  ('13:40:06', '14:40:06', 'fun'), ('14:40:09', '15:40:09', 'work')]
