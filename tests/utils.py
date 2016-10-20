import os

import django
from django.conf import settings
from django.utils import six

try:
    from django.test import override_settings
except ImportError:
    # Django < 1.7
    from django.test.utils import override_settings


def _(path):
    # Make sure the path contains only the correct separator
    return path.replace('/', os.sep).replace('\\', os.sep)


class pipeline_settings(override_settings):
    def __init__(self, **kwargs):
        if django.VERSION[:2] >= (1, 10):
            # Django 1.10's override_settings inherits from TestContextDecorator
            # and its __init__ method calls its superclass' __init__ method too,
            # so we must do the same.
            super(pipeline_settings, self).__init__()
        self.options = {'PIPELINE': kwargs}


# Django < 1.7 (copy-pasted from Django 1.7)
class modify_settings(override_settings):
    """
    Like override_settings, but makes it possible to append, prepend or remove
    items instead of redefining the entire list.
    """
    def __init__(self, *args, **kwargs):
        if args:
            # Hack used when instantiating from SimpleTestCase._pre_setup.
            assert not kwargs
            self.operations = args[0]
        else:
            assert not args
            self.operations = list(kwargs.items())

    def save_options(self, test_func):
        if test_func._modified_settings is None:
            test_func._modified_settings = self.operations
        else:
            # Duplicate list to prevent subclasses from altering their parent.
            test_func._modified_settings = list(
                test_func._modified_settings) + self.operations

    def enable(self):
        self.options = {}
        for name, operations in self.operations:
            try:
                # When called from SimpleTestCase._pre_setup, values may be
                # overridden several times; cumulate changes.
                value = self.options[name]
            except KeyError:
                value = list(getattr(settings, name, []))
            for action, items in operations.items():
                # items my be a single value or an iterable.
                if isinstance(items, six.string_types):
                    items = [items]
                if action == 'append':
                    value = value + [item for item in items if item not in value]
                elif action == 'prepend':
                    value = [item for item in items if item not in value] + value
                elif action == 'remove':
                    value = [item for item in value if item not in items]
                else:
                    raise ValueError("Unsupported action: %s" % action)
            self.options[name] = value
        super(modify_settings, self).enable()
