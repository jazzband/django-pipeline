import mimetypes
import os
import sys
import urllib

from django.utils import importlib
from django.utils.encoding import smart_str

from pipeline.conf import settings


def to_class(class_str):
    if not class_str:
        return None

    module_bits = class_str.split('.')
    module_path, class_name = '.'.join(module_bits[:-1]), module_bits[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_name, None)


def filepath_to_uri(path):
    if path is None:
        return path
    return urllib.quote(smart_str(path).replace("\\", "/"), safe="/~!*()'#?")


def guess_type(path, default=None):
    for type, ext in settings.PIPELINE_MIMETYPES:
        mimetypes.add_type(type, ext)
    mimetype, _ = mimetypes.guess_type(path)
    if not mimetype:
        return default
    return mimetype


def _relpath_nt(path, start=os.path.curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError("no path specified")
    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)
    if start_list[0].lower() != path_list[0].lower():
        unc_path, rest = os.path.splitunc(path)
        unc_start, rest = os.path.splitunc(start)
        if bool(unc_path) ^ bool(unc_start):
            raise ValueError("Cannot mix UNC and non-UNC paths (%s and %s)"
                                                                % (path, start))
        else:
            raise ValueError("path is on drive %s, start on drive %s"
                                                % (path_list[0], start_list[0]))
    # Work out how much of the filepath is shared by start and path.
    for i in range(min(len(start_list), len(path_list))):
        if start_list[i].lower() != path_list[i].lower():
            break
    else:
        i += 1

    rel_list = [os.path.pardir] * (len(start_list) - i) + path_list[i:]
    if not rel_list:
        return os.path.curdir
    return os.path.join(*rel_list)


def _relpath_posix(path, start=os.path.curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))

    rel_list = [os.path.pardir] * (len(start_list) - i) + path_list[i:]
    if not rel_list:
        return os.path.curdir
    return os.path.join(*rel_list)


if os.path is sys.modules.get('ntpath'):
    relpath = _relpath_nt
else:
    relpath = _relpath_posix
