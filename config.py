from pathlib import Path
from datetime import datetime

# format for dates (appear sorted in directory)
form = '%Y-%m-%d'

# path to JSON files
path = str(Path(__file__).parent) + '/'
log_path = path + 'log/'

# start date from tracking
start_date = datetime.strptime('2021-07-27', '%Y-%m-%d')

# keywords for each tag
tag_to_keys = {
    'Programming': ['william', 'IPython', 'Source.gv', 'Stack Overflow', 'python', 'Python', 'dataschool',
                    'Stack Exchange', 'GitHub', 'github', 'fish', 'autotimer', 'Autotimer', 'TimeNazi'],
    'Book': ['book.lyx', 'book.pdf', 'Inkscape', 'Ayoa', 'Thoughts on Artificial General Intelligence', 'latex',
             'Figure', 'Causal deconvolution', 'frai-2020', 'Zenil', 'algorithmic complexity', 'jphysparis',
             'free-energy', 'aixi_approx', 'neco_a_00999.pdf'],
    'Thinking': ['thoughts_on_AGI', 'Gedanken'],
}

# JSON file storing the target time to spend on each tag
target_file = 'target.json'

# time you want to spend on those tasks (tags) every day (in hours)
workday_target = {
    'Programming': [4, None],
    'Book': [1, None],
    'Thinking': [1, None],
}

free_weekdays = [5, 6]  # Saturday = 5, Sunday = 6

holiday_target = {
    'Programming': [0, None],
    'Book': [0, None],
    'Thinking': [0, None],
}
