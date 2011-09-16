import os
import re

from django.core.cache import cache

from pipeline.conf import settings
from pipeline.storage import storage
from pipeline.utils import to_class


class Versioning(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def versioner(self):
        return to_class(settings.PIPELINE_VERSIONING)(self)
    versioner = property(versioner)

    def version(self, paths):
        return getattr(self.versioner, 'version')(paths)

    def version_from_file(self, path, filename, force=False):
        version = cache.get("pipeline:%s" % filename)
        if (not version) or force:
            filename = settings.PIPELINE_VERSION_PLACEHOLDER.join([re.escape(part)
                for part in filename.split(settings.PIPELINE_VERSION_PLACEHOLDER)])
            regex = re.compile(r'^%s$' % self.output_filename(filename, r'([A-Za-z0-9]+)'))
            for f in sorted(storage.listdir(path)[1], reverse=True):
                match = regex.match(f)
                if match and match.groups():
                    version = match.group(1)
                    break
            cache.set("pipeline:%s" % filename, version, settings.PIPELINE_CACHE_TIMEOUT)
        return str(version)

    def output_filename(self, filename, version):
        if settings.PIPELINE_VERSION and version is not None:
            return filename.replace(settings.PIPELINE_VERSION_PLACEHOLDER,
                version)
        else:
            return filename.replace(settings.PIPELINE_VERSION_PLACEHOLDER,
                settings.PIPELINE_VERSION_DEFAULT)

    def need_update(self, output_file, paths):
        version = self.version(paths)
        output_file = self.output_filename(output_file, version)
        return getattr(self.versioner, 'need_update')(output_file, paths, version)

    def cleanup(self, filename):
        if not (settings.PIPELINE_VERSION and settings.PIPELINE_VERSION_REMOVE_OLD):
            return  # Nothing to delete here
        path = os.path.dirname(filename)
        filename = os.path.basename(filename)
        filename = settings.PIPELINE_VERSION_PLACEHOLDER.join([re.escape(part)
            for part in filename.split(settings.PIPELINE_VERSION_PLACEHOLDER)])
        regex = re.compile(r'^%s$' % self.output_filename(filename, r'([A-Za-z0-9]+)'))
        try:
            for f in storage.listdir(path)[1]:
                if regex.match(f):
                    if self.verbose:
                        print "Removing outdated file %s" % f
                    storage.delete(os.path.join(path, f))
        except EnvironmentError:
            # We can't use exists() first because some backends (S3) have no concept of directories.
            pass


class VersioningBase(object):
    def __init__(self, versioning):
        self.versioning = versioning

    def output_filename(self, filename, version):
        return self.versioning.output_filename(filename, version)

    def version(self, source_files):
        raise NotImplementedError

    def needs_update(self, output_file, paths, version):
        raise NotImplementedError


class VersioningError(Exception):
    """This exception is raised when version creation fails"""
    pass
