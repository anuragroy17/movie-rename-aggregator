import os


def folders():
    DIRECTORY = 1
    return next(os.walk(os.curdir))[DIRECTORY]


def rename(path_from, path_to):
    absolute_from = os.path.join(os.getcwd(), path_from)
    absolute_to = os.path.join(os.getcwd(), path_to)
    try:
        os.rename(absolute_from, absolute_to)
        return True
    except:
        return False
