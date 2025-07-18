import re

def classify_file(filename: str) -> str:
    name = filename.lower()

    if re.search(r'func|bold|run\d|task', name):
        return 'raw/func'
    elif re.search(r't1w|anat|mprage|sag|brain', name):
        return 'raw/anat'
    elif re.search(r'proto|questionnaire|survey|form|json', name):
        return 'protocols'
    elif name.endswith(('.txt', '.tsv', '.csv')):
        return 'meta'
    elif 'log' in name or 'scaninfo' in name:
        return 'logs'
    else:
        return 'unsorted'
