from __future__ import unicode_literals

import sys
import mimetypes
import posixpath

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from django.utils import six
from django.utils.encoding import smart_str

from pipeline.conf import settings


if six.PY3:
    from importlib import import_module
else:
    def _resolve_name(name, package, level):
        """Return the absolute name of the module to be imported."""
        if not hasattr(package, 'rindex'):
            raise ValueError("'package' not set to a string")
        dot = len(package)
        for x in range(level, 1, -1):
            try:
                dot = package.rindex('.', 0, dot)
            except ValueError:
                raise ValueError("attempted relative import beyond top-level package")
        return "%s.%s" % (package[:dot], name)

    def import_module(name, package=None):
        """Import a module.

        The 'package' argument is required when performing a relative import. It
        specifies the package to use as the anchor point from which to resolve the
        relative import to an absolute import.

        """
        if name.startswith('.'):
            if not package:
                raise TypeError("relative imports require the 'package' argument")
            level = 0
            for character in name:
                if character != '.':
                    break
                level += 1
            name = _resolve_name(name[level:], package, level)
        __import__(name)
        return sys.modules[name]


def to_class(class_str):
    if not class_str:
        return None

    module_bits = class_str.split('.')
    module_path, class_name = '.'.join(module_bits[:-1]), module_bits[-1]
    module = import_module(module_path)
    return getattr(module, class_name, None)


def filepath_to_uri(path):
    if path is None:
        return path
    return quote(smart_str(path).replace("\\", "/"), safe="/~!*()'#?")


def guess_type(path, default=None):
    for type, ext in settings.PIPELINE_MIMETYPES:
        mimetypes.add_type(type, ext)
    mimetype, _ = mimetypes.guess_type(path)
    if not mimetype:
        return default
    return smart_str(mimetype)


def relpath(path, start=posixpath.curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError("no path specified")

    start_list = posixpath.abspath(start).split(posixpath.sep)
    path_list = posixpath.abspath(path).split(posixpath.sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(posixpath.commonprefix([start_list, path_list]))

    rel_list = [posixpath.pardir] * (len(start_list) - i) + path_list[i:]
    if not rel_list:
        return posixpath.curdir
    return posixpath.join(*rel_list)
