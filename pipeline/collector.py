from __future__ import unicode_literals

import os

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

from pipeline.finders import PipelineFinder


class Collector(object):
    def __init__(self, storage=None):
        if storage is None:
            storage = staticfiles_storage
        self.storage = storage

    def clear(self, path=""):
        dirs, files = self.storage.listdir(path)
        for f in files:
            fpath = os.path.join(path, f)
            self.storage.delete(fpath)
        for d in dirs:
            self.clear(os.path.join(path, d))

    def collect(self):
        found_files = OrderedDict()
        for finder in finders.get_finders():
            # Ignore our finder to avoid looping
            if isinstance(finder, PipelineFinder):
                continue
            for path, storage in finder.list(['CVS', '.*', '*~']):
                # Prefix the relative path if the source storage contains it
                if getattr(storage, 'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path
                if prefixed_path not in found_files:
                    found_files[prefixed_path] = (storage, path)
                    self.copy_file(path, prefixed_path, storage)

    def copy_file(self, path, prefixed_path, source_storage):
        # Delete the target file if needed or break
        if not self.delete_file(path, prefixed_path, source_storage):
            return
        # Finally start copying
        with source_storage.open(path) as source_file:
            self.storage.save(prefixed_path, source_file)

    def delete_file(self, path, prefixed_path, source_storage):
        if self.storage.exists(prefixed_path):
            try:
                # When was the target file modified last time?
                target_last_modified = self.storage.modified_time(prefixed_path)
            except (OSError, NotImplementedError, AttributeError):
                # The storage doesn't support ``modified_time`` or failed
                pass
            else:
                try:
                    # When was the source file modified last time?
                    source_last_modified = source_storage.modified_time(path)
                except (OSError, NotImplementedError, AttributeError):
                    pass
                else:
                    # Skip the file if the source file is younger
                    # Avoid sub-second precision
                    if (target_last_modified.replace(microsecond=0)
                            >= source_last_modified.replace(microsecond=0)):
                            return False
            # Then delete the existing file if really needed
            self.storage.delete(prefixed_path)
        return True

default_collector = Collector()
