import contextlib
import os

from pipeline.conf import settings


def _(path):
    # Make sure the path contains only the correct separator
    return path.replace('/', os.sep).replace('\\', os.sep)


@contextlib.contextmanager
def pipeline_settings(**kwargs):
    try:
        saved = {}
        for name, value in kwargs.items():
            saved[name] = getattr(settings, name)
            setattr(settings, name, value)
        yield
    finally:
        for name, value in saved.items():
            setattr(settings, name, value)
