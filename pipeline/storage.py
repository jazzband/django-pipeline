from __future__ import unicode_literals

import gzip
import tempfile

from io import BytesIO

from django.contrib.staticfiles.storage import CachedStaticFilesStorage, StaticFilesStorage
from django.contrib.staticfiles.utils import matches_patterns

from django.core.files.base import File

from pipeline.conf import settings


class PipelineMixin(object):
    packing = True

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        from pipeline.packager import Packager
        packager = Packager(storage=self)
        for package_name in packager.packages['css']:
            package = packager.package_for('css', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_stylesheets(package)
            paths[output_file] = (self, output_file)
            yield output_file, output_file, True
        for package_name in packager.packages['js']:
            package = packager.package_for('js', package_name)
            output_file = package.output_filename
            if self.packing:
                packager.pack_javascripts(package)
            paths[output_file] = (self, output_file)
            yield output_file, output_file, True

        super_class = super(PipelineMixin, self)
        if hasattr(super_class, 'post_process'):
            for name, hashed_name, processed in super_class.post_process(paths.copy(), dry_run, **options):
                yield name, hashed_name, processed

    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name


class GZIPMixin(object):
    gzip_patterns = ("*.css", "*.js")

    def _compress(self, original_file):
        content = BytesIO()
        gzip_file = gzip.GzipFile(mode='wb', fileobj=content)
        gzip_file.write(original_file.read())
        gzip_file.close()
        content.seek(0)
        return File(content)

    def post_process(self, paths, dry_run=False, **options):
        super_class = super(GZIPMixin, self)
        if hasattr(super_class, 'post_process'):
            for name, hashed_name, processed in super_class.post_process(paths.copy(), dry_run, **options):
                if hashed_name != name:
                    paths[hashed_name] = (self, hashed_name)
                yield name, hashed_name, processed

        if dry_run:
            return

        for path in paths:
            if path:
                if not matches_patterns(path, self.gzip_patterns):
                    continue
                original_file = self.open(path)
                gzipped_path = "{0}.gz".format(path)
                if self.exists(gzipped_path):
                    self.delete(gzipped_path)
                gzipped_file = self._compress(original_file)
                gzipped_path = self.save(gzipped_path, gzipped_file)
                yield gzipped_path, gzipped_path, True


class NonPackagingMixin(object):
    packing = False


class PipelineStorage(PipelineMixin, StaticFilesStorage):
    pass


class NonPackagingPipelineStorage(NonPackagingMixin, PipelineStorage):
    pass


class PipelineCachedStorage(PipelineMixin, CachedStaticFilesStorage):
    pass


class NonPackagingPipelineCachedStorage(NonPackagingMixin, PipelineCachedStorage):
    pass
