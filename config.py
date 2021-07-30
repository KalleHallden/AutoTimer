from datetime import datetime

# format for dates (appear sorted in directory)
form = '%Y-%m-%d'

# relative path to JSON files
path = 'log/'

# start date from tracking
start_date = datetime.strptime('2021-07-27', '%Y-%m-%d')

# keywords for each tag
tag_to_keys = {
    'Programming': ['william', 'IPython', 'Source.gv', 'Stack Overflow', 'python', 'Python', 'dataschool',
                    'Stack Exchange', 'GitHub', 'github', 'fish', 'autotimer'],
    'Book': ['book.lyx', 'book.pdf', 'Inkscape'],
    'Thinking': ['thoughts_on_AGI', 'Gedanken'],
}

# JSON file storing the target time to spend on each tag
target_file = 'target.json'

# time you want to spend on those tasks (tags) every day (in hours)
default_target = {
    'Programming': 4,
    'Book': 1,
    'Thinking': 1,
}
