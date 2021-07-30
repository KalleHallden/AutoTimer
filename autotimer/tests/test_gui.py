from ..gui import TimerGUI
from ..stats import get_stats


def test_hovering():
    times = get_stats()
    root = TimerGUI(times)
    root.mainloop()
