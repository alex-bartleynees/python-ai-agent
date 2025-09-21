import os


def is_subpath(path, base):
    path = os.path.abspath(path)
    base = os.path.abspath(base)
    return os.path.commonpath([base]) == os.path.commonpath([path, base])
