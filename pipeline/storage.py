from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import CachedStaticFilesStorage, StaticFilesStorage
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject


from pipeline.conf import settings


class BaseFinderStorage(StaticFilesStorage):
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


class PipelineStorage(CachedStaticFilesStorage):
    def post_process(self, paths, dry_run=False, **options):
        from pipeline.packager import Packager
        if dry_run:
            return []
        packager = Packager()
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = packager.pack_stylesheets(package)
            paths.append(output_file)
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = packager.pack_javascripts(package)
            paths.append(output_file)
        return super(PipelineStorage, self).post_process(paths, dry_run, **options)


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


storage = DefaultStorage()
