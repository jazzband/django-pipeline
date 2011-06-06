import os

from datetime import datetime

from django.core.files.storage import FileSystemStorage, get_storage_class
from django.utils.functional import LazyObject

from pipeline.conf import settings


class PipelineStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.PIPELINE_ROOT
        if base_url is None:
            base_url = settings.PIPELINE_URL
        super(PipelineStorage, self).__init__(location, base_url, *args, **kwargs)

    def accessed_time(self, name):
        return datetime.fromtimestamp(os.path.getatime(self.path(name)))

    def created_time(self, name):
        return datetime.fromtimestamp(os.path.getctime(self.path(name)))

    def modified_time(self, name):
        return datetime.fromtimestamp(os.path.getmtime(self.path(name)))


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


storage = DefaultStorage()
