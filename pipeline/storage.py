import errno
import os

from datetime import datetime

try:
    from django.contrib.staticfiles import finders
except ImportError:
    from staticfiles import finders

from django.core.exceptions import ImproperlyConfigured
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

    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name

    def _open(self, name, mode='rb'):
        full_path = self.path(name)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)
        return super(PipelineStorage, self)._open(name, mode)


class BaseFinderStorage(PipelineStorage):
    finders = None

    def __init__(self, finders=None, *args, **kwargs):
        if finders is not None:
            self.finders = finders
        if self.finders is None:
            raise ImproperlyConfigured("The storage %r doesn't have a finders class assigned." % self.__class__)
        super(BaseFinderStorage, self).__init__(*args, **kwargs)

    def path(self, name):
        path = self.finders.find(name)
        if not path:
            path = super(BaseFinderStorage, self).path(name)
        return path

    def exists(self, name):
        exists = self.finders.find(name) != None
        if not exists:
            exists = super(BaseFinderStorage, self).exists(name)
        return exists


class PipelineFinderStorage(BaseFinderStorage):
    finders = finders


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


storage = DefaultStorage()
