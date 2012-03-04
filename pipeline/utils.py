import urllib

from django.utils import importlib
from django.utils.encoding import smart_str


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
