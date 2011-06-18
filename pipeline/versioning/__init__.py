import os
import re

from pipeline.conf import settings
from pipeline.storage import storage
from pipeline.utils import to_class


class Versioning(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def versionner(self):
        return to_class(settings.PIPELINE_VERSIONING)(self)
    versionner = property(versionner)

    def version(self, paths):
        return getattr(self.versionner, 'version')(paths)

    def version_from_file(self, path, filename):
        filename = settings.PIPELINE_VERSION_PLACEHOLDER.join([re.escape(part) for part in filename.split(settings.PIPELINE_VERSION_PLACEHOLDER)])
        regex = re.compile(r'^%s$' % self.output_filename(filename, r'([A-Za-z0-9]+)'))
        versions = []
        for f in sorted(storage.listdir(path)[1], reverse=True):
            version = regex.match(f)
            if version and version.groups():
                versions.append(version.group(1))
        versions.sort()
        return versions[-1]

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
        if not storage.exists(output_file):
            return True, version
        return getattr(self.versionner, 'need_update')(output_file, paths, version)

    def cleanup(self, filename):
        if not settings.PIPELINE_VERSION and not settings.PIPELINE_VERSION_REMOVE_OLD:
            return  # Nothing to delete here
        path = os.path.dirname(filename)
        filename = settings.PIPELINE_VERSION_PLACEHOLDER.join([re.escape(part) for part in filename.split(settings.PIPELINE_VERSION_PLACEHOLDER)])
        regex = re.compile(r'^%s$' % os.path.basename(self.output_filename(filename, r'([A-Za-z0-9]+)')))
        if storage.exists(path):
            for f in storage.listdir(path)[1]:
                if regex.match(f):
                    if self.verbose:
                        print "Removing outdated file %s" % f
                    storage.delete(os.path.join(path, f))


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
