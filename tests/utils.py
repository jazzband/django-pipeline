import os

import django

from django.test import override_settings


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
