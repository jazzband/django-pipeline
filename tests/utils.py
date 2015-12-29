import os

from django.test import override_settings


def _(path):
    # Make sure the path contains only the correct separator
    return path.replace('/', os.sep).replace('\\', os.sep)


class pipeline_settings(override_settings):
    def __init__(self, **kwargs):
        self.options = {'PIPELINE': kwargs}
