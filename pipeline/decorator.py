# -*- coding: utf-8 -*-
from __future__ import unicode_literals

""" 
    This code is a part of django.utils.six on https://github.com/django/django/blob/stable/2.2.x/django/utils/six.py removed form Django 3.0
    To keep the backward compatibility between python 2 and 3 the decorator need to be used as well, during the time we find a proper way to 
    handle MetaClass overwright working on both versions (or dropping python 2 support).
"""

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper