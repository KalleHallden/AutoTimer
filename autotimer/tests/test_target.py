from datetime import datetime

from ..target import Target


def test_sum_by_tag():
    end_date = datetime(year=2021, month=7, day=29)
    t = Target(filename='test_target.json', end_date=end_date)
    targ = t.sum_by_tag()
    expected = {'Book': [6, '1:09:23'],
                'Programming': [12, '8:21:20'],
                'Thinking': [2, '1:26:36']}
    for tag, (hours, actual_time) in targ.items():
        assert [hours, str(actual_time)] == expected[tag]
