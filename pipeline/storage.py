import os

try:
    from staticfiles import finders
    from staticfiles.storage import CachedFilesMixin, StaticFilesStorage
except ImportError:
    from django.contrib.staticfiles import finders # noqa
    from django.contrib.staticfiles.storage import CachedFilesMixin, StaticFilesStorage # noqa

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject

from pipeline.conf import settings


class PipelineMixin(object):
    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return []

        from pipeline.packager import Packager
        packager = Packager(storage=self)
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = packager.pack_stylesheets(package)
            paths[output_file] = (self, output_file)
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = packager.pack_javascripts(package)
            paths[output_file] = (self, output_file)

        super_class = super(PipelineMixin, self)
        if hasattr(super_class, 'post_process'):
            return super_class.post_process(paths, dry_run, **options)

        return [
            (path, path, True)
            for path in paths
        ]

    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name


class PipelineStorage(PipelineMixin, StaticFilesStorage):
    pass


class PipelineCachedStorage(PipelineMixin, CachedFilesMixin, StaticFilesStorage):
    pass


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

    def listdir(self, path):
        for finder in finders.get_finders():
            for storage in finder.storages.values():
                try:
                    return storage.listdir(path)
                except OSError:
                    pass

    def _save(self, name, content):
        for finder in finders.get_finders():
            for path, storage in finder.list([]):
                if os.path.dirname(name) in path:
                    return storage._save(name, content)


class PipelineFinderStorage(BaseFinderStorage):
    finders = finders


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


default_storage = DefaultStorage()
