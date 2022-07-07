import re


def strip_quality(path):
    path, brcount = re.subn('brrip$', '', path, count=0, flags=re.IGNORECASE)
    path, dvdcount = re.subn('dvdrip$', '', path, count=0, flags=re.IGNORECASE)
    rip = ''
    if brcount == 1:
        rip = ' BRRip'
    elif dvdcount == 1:
        rip = ' DVDRip'

    return path, rip


def get_name_from_folder(path):
    path = re.sub('^[12][0-9]{3}', '', path)
    path = path.rstrip(') ')
    path = re.sub('[12][0-9]{3}$', '', path)
    path = path.strip('() ')
    return path


def get_year_from_folder(path):
    x = re.search('.*([1-3][0-9]{3})', path)
    year = None
    if bool(x):
        year = x.group(1)
    return bool(x), year


def strip_after(string, character):
    position = string.rfind(character)
    if position > 0:
        string = string[:position]
    return string


def replace_colon(title):
    return title.replace(":", " -")


def compare_titles(local, fetched):
    local = strip_after(local, '-')
    local = strip_after(local, ':')
    fetched = strip_after(fetched, '-')
    fetched = strip_after(fetched, ':')
    ignore = '[-.,()\'" ]+'
    local = re.sub(ignore, '', local).lower()
    fetched = re.sub(ignore, '', fetched).lower()
    return local == fetched


def user_decision_for_rename(name, title):
    letter = None
    while not (letter == 'n' or letter == 'y'):
        letter = input('> Rename \'' + name +
                       '\' to \'' + title + '\'? (y/n) ')
    return letter == 'y'


def user_decision_for_service():
    letter = None
    while not (letter == 'a' or letter == 'b'):
        letter = input('''> use which service?
        a) Imdb Page Scrapping (faster)
        b) Cinemagoer ImdbPy
        
        Select a/b ''')
    return letter


def print_line(folder, year, title, rename_to, action):
    def format(string, length=35):
        if len(string) > length:
            return string[:length-3] + '...'
        else:
            return string.ljust(length)
    print(format(folder), year.ljust(4), format(
        title), format(rename_to), action, flush=True)


def print_change(folder, year, title, output, action):
    print_line(folder, year, title, output, action)


# not used
def has_year(path):
    left = re.compile('^[1-2][0-9]{3}')
    right = re.compile('[1-2][0-9]{3}$')
    path = re.sub('[()]', '', path)
    path = path.strip()
    return left.match(path) or right.match(path)


def remove_subtitle(title):
    title = strip_after(title, '-')
    title = strip_after(title, ':')
    title = title.rstrip(' ')
    return title
