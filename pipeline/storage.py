from __future__ import unicode_literals

import gzip
import hashlib
import io
import os

from io import BytesIO

from django.contrib.staticfiles.storage import CachedStaticFilesStorage, StaticFilesStorage
from django.contrib.staticfiles.utils import matches_patterns

from django.core.files.base import File


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

    def get_available_name(self, name, max_length=None):
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


class OptimizedPipelineStorage(PipelineMixin, StaticFilesStorage):
    """This storage compresses only the packages which had modifications in
    their source files, or that have not been compressed yet. This speeds up
    the collectstatic process, since must of the time we modify only a few
    javascript/css files at a time.

    It also appends the a md5 hash to the compressed files' url so any existing
    cache mechanisms are naturally invalidated."""

    compressed_packages = []
    unchanged_packages = []
    packager = None
    HASH_CACHE_KEY = 'pipeline_compressed_hash_key'
    SOURCES_DUMP_KEY = 'pipeline_dumped_sources_key'

    def url(self, name):
        """Append the produced hash to the resource url so existing cache
        mechanisms are naturally invalidated."""
        url = super(OptimizedPipelineStorage, self).url(name)
        _hash = self.get_compressed_files_hash()
        if _hash and name:
            return '{url}?{_hash}'.format(url=url, _hash=_hash)
        else:
            return url

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        from pipeline.packager import Packager
        self.packager = Packager(storage=self)

        for package_name in self.packager.packages['css']:
            package = self.packager.package_for('css', package_name)
            output_file = package.output_filename

            if self.packing and self._is_outdated(package_name, package):
                print('COMPRESSING {} package...'.format(package_name))
                self.packager.pack_stylesheets(package)
                self.compressed_packages.append(package_name)
            else:
                self.unchanged_packages.append(package_name)

            paths[output_file] = (self, output_file)
            yield output_file, output_file, True

        for package_name in self.packager.packages['js']:
            package = self.packager.package_for('js', package_name)
            output_file = package.output_filename

            if self.packing and self._is_outdated(package_name, package):
                print('COMPRESSING {} package...'.format(package_name))
                self.packager.pack_javascripts(package)
                self.compressed_packages.append(package_name)
            else:
                self.unchanged_packages.append(package_name)

            paths[output_file] = (self, output_file)
            yield output_file, output_file, True

        super_class = super(PipelineMixin, self)
        if hasattr(super_class, 'post_process'):
            for name, hashed_name, processed in super_class.post_process(
                    paths.copy(), dry_run, **options):
                yield name, hashed_name, processed

        self._finalize()

    def _is_outdated(self, package_name, package):
        outdated = False

        for path in package.paths:
            # Needs to run for every path in order to generate the individual
            # file hashes.
            if self._is_content_changed(path) and not outdated:
                outdated = True

        if not outdated:
            previous_paths = self._get_previous_compressed_sources(package_name)
            if not previous_paths or set(previous_paths) != set(package.paths):
                outdated = True

        from django.conf import settings
        output_path = os.path.join(settings.STATIC_ROOT, package.output_filename)
        return outdated or not os.path.exists(output_path)

    def _is_content_changed(self, path):
        """Verifies if the content of :path change based on the hash that was
        produced during the last collecstatic run."""
        from django.conf import settings
        changed = True
        infile_path = os.path.join(self.location, path)
        outfile_path = os.path.join(settings.STATIC_ROOT, path)
        infile_hash_path = outfile_path + '.hash'

        with open(infile_path, 'rb') as infile_file:
            current_hash = hashlib.md5(infile_file.read()).hexdigest()

        from django.core.cache import caches
        DEFAULT_CACHE = caches['default']
        old_hash = DEFAULT_CACHE.get(infile_hash_path)
        changed = current_hash != old_hash
        DEFAULT_CACHE.set(infile_hash_path, current_hash, None)
        return changed

    def _finalize(self):
        self._dump_sources()
        print('\n=== {} results ==='.format(self.__class__.__name__))
        total_removed = self._remove_sources()
        self._write_hash()
        print('{} removed files used in the compressing'.format(total_removed))
        print('{} new compressed packages: {}'.format(
            len(self.compressed_packages), self.compressed_packages))
        print('{} unchanged packages: {}'.format(
            len(self.unchanged_packages), self.unchanged_packages))
        print('=== End {} results ==='.format(self.__class__.__name__))

    def _remove_sources(self):
        """We do not want to expose our source files, thus they are removed
        from the STATIC_ROOT directory, keeping only the compressed files."""
        from django.conf import settings
        sources = []

        for package_name in self.packager.packages['js']:
            package = self.packager.package_for('js', package_name)
            sources.extend(package.paths)

        for package_name in self.packager.packages['css']:
            package = self.packager.package_for('css', package_name)
            sources.extend(package.paths)

        removed = 0
        for source in sources:
            source_path = os.path.join(settings.STATIC_ROOT, source)
            if os.path.exists(source_path):
                os.remove(source_path)
                removed += 1

        return removed

    def _dump_sources(self):
        """We dump the list of compressed source files so we can compare if
        there is any difference (new files or removed files) in the next
        collectstatic run."""
        from django.core.cache import caches
        DEFAULT_CACHE = caches['default']

        packages = {}

        for package_name in self.packager.packages['js']:
            package = self.packager.package_for('js', package_name)
            packages[package_name] = package.paths

        for package_name in self.packager.packages['css']:
            package = self.packager.package_for('css', package_name)
            packages[package_name] = package.paths
            # cache forever
            DEFAULT_CACHE.set(self.SOURCES_DUMP_KEY, packages, None)

    def _get_previous_compressed_sources(self, package_name):
        from django.core.cache import caches
        DEFAULT_CACHE = caches['default']
        return DEFAULT_CACHE.get(self.SOURCES_DUMP_KEY, {}).\
            get(package_name)

    def _write_hash(self):
        """Writes a single md5 hash considering all the content from the
        source files. This is useful to force any cache mechanism to update
        their registries."""
        from django.conf import settings
        from django.core.cache import caches
        DEFAULT_CACHE = caches['default']
        output_filenames = []

        for package_name in self.packager.packages['js']:
            package = self.packager.package_for('js', package_name)
            output_filenames.append(package.output_filename)

        for package_name in self.packager.packages['css']:
            package = self.packager.package_for('css', package_name)
            output_filenames.append(package.output_filename)

        contents = []
        for output_filename in output_filenames:
            abs_path = os.path.join(settings.STATIC_ROOT, output_filename)
            with io.open(abs_path, 'rb') as output_file:
                contents.append(output_file.read())

        digest = hashlib.md5(b''.join(contents)).hexdigest()
        print('New hash: {}'.format(digest))
        DEFAULT_CACHE.set(self.HASH_CACHE_KEY, digest, None)  # cache forever

    @staticmethod
    def get_compressed_files_hash():
        from django.core.cache import caches
        DEFAULT_CACHE = caches['default']
        return DEFAULT_CACHE.get(OptimizedPipelineStorage.HASH_CACHE_KEY)
