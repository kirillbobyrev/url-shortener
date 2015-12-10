import os

os.system('touch storage.txt')

FILENAME = os.path.dirname(os.path.realpath(__file__)) + '/storage.txt'


def load_entries_from_storage_():
    with open(FILENAME, 'r', encoding='utf-8') as storage:
        return eval(storage.read())


def update_storage_():
    with open(FILENAME, 'w') as storage:
        print(repr(entries_), file=storage)

entries_ = load_entries_from_storage_()


def get_entries():
    return entries_


def add_entry(entry):
    entries_.append(entry)
    update_storage_()


def get_answer(short_url):
    for entry in entries_:
        if short_url == entry['short_url']:
            return entry['long_url']
    return False
