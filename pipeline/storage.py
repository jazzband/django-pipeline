try:
    from staticfiles.storage import CachedStaticFilesStorage, StaticFilesStorage
except ImportError:
    from django.contrib.staticfiles.storage import CachedStaticFilesStorage, StaticFilesStorage

from django.core.files.storage import get_storage_class
from django.utils.functional import LazyObject

from pipeline.conf import settings


class PipelineStorage(StaticFilesStorage):
    def post_process(self, paths, dry_run=False, **options):
        from pipeline.packager import Packager
        if dry_run:
            return []

        packager = Packager()
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            for path in package['paths']:
                if path in paths:
                    paths.remove(path)
            output_file = packager.pack_stylesheets(package)
            paths.append(output_file)
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            for path in package['paths']:
                if path in paths:
                    paths.remove(path)
            output_file = packager.pack_javascripts(package)
            paths.append(output_file)
        return super(PipelineStorage, self).post_process(paths, dry_run, **options)


class PipelineCachedStorage(PipelineStorage, CachedStaticFilesStorage):
    pass


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(settings.PIPELINE_STORAGE)()


storage = DefaultStorage()
