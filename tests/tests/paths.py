import os


def _(path):
    # Make sure the path contains only the correct separator
    return path.replace('/', os.sep).replace('\\', os.sep)
