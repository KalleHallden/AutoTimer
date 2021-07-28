from datetime import datetime

# format for dates
form = '%Y-%m-%d'

# relative path to JSON files
path = 'log/'

# start date from tracking
start_date = datetime.strptime('2021-07-27', '%Y-%m-%d')

# JSON file storing the target time to spend on each tag
target_file = 'target.json'


# keywords for each tag
tag_to_keys = {
    'Programming': ['william', 'IPython', 'Source.gv', 'Stack Overflow', 'python', 'Python'],
    'Book': ['book.lyx', 'book.pdf', 'Inkscape'],
    'Thinking': ['thoughts_on_AGI.lyx'],
}


# default target for every day (in hours)
default_target = {
    'Programming': 4,
    'Book': 1,
    'Thoughts': 1,
}
