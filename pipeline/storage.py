from __future__ import unicode_literals

import os

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import CachedFilesMixin, StaticFilesStorage

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject

from pipeline.conf import settings


class PipelineMixin(object):
    packing = True

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return []

        from pipeline.packager import Packager
        packager = Packager(storage=self)
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_stylesheets(package)
            paths[output_file] = (self, output_file)
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_javascripts(package)
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


class NonPackagingMixin(object):
    packing = False


class PipelineStorage(PipelineMixin, StaticFilesStorage):
    pass


class NonPackagingPipelineStorage(NonPackagingMixin, PipelineStorage):
    pass


class PipelineCachedStorage(PipelineMixin, CachedFilesMixin, StaticFilesStorage):
    pass


class NonPackagingPipelineCachedStorage(NonPackagingMixin, PipelineCachedStorage):
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
        exists = self.finders.find(name) is not None
        if not exists:
            return super(BaseFinderStorage, self).exists(name)
        return exists

    def listdir(self, path):
        for finder in self.finders.get_finders():
            for storage in finder.storages.values():
                try:
                    return storage.listdir(path)
                except OSError:
                    pass

    def match_location(self, name, path, prefix=None):
        if prefix:
            if prefix != name[:len(prefix)]:
                return None
            prefix = "%s%s" % (prefix, os.sep)
            name = name[len(prefix):]

        norm_path = os.path.normpath(path)
        norm_name = os.path.normpath(name)

        if norm_path == norm_name:
            return name
        if os.path.splitext(norm_path)[0] == os.path.splitext(norm_name)[0]:
            return name
        return None

    def find_storage(self, name):
        for finder in self.finders.get_finders():
            for path, storage in finder.list([]):
                prefix = getattr(storage, 'prefix', None)
                matched_path = self.match_location(name, path, prefix)
                if matched_path:
                    return matched_path, storage
        raise ValueError("The file '%s' could not be found with %r." % (name, self))

    def _open(self, name, mode="rb"):
        name, storage = self.find_storage(name)
        return storage._open(name, mode)

    def _save(self, name, content):
        name, storage = self.find_storage(name)
        # Ensure we overwrite file, since we have no control on external storage
        if storage.exists(name):
            storage.delete(name)
        return storage._save(name, content)


class PipelineFinderStorage(BaseFinderStorage):
    finders = finders


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


default_storage = DefaultStorage()
