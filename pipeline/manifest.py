from __future__ import unicode_literals

import os

from django.contrib.staticfiles.finders import get_finders
from django.conf import settings as dj_settings

from pipeline.conf import settings
from pipeline.storage import PipelineCachedStorage

from manifesto import Manifest

from pipeline.packager import Packager


class PipelineManifest(Manifest):
    def __init__(self):
        self.packager = Packager()
        self.packages = self.collect_packages()
        self.finders = get_finders()
        self.package_files = []
        if dj_settings.STATICFILES_STORAGE == \
                'pipeline.storage.PipelineCachedStorage':
            self.pcs = PipelineCachedStorage()
        else:
            self.pcs = None

    def collect_packages(self):
        packages = []
        for package_name in self.packager.packages['css']:
            package = self.packager.package_for('css', package_name)
            if package.manifest:
                packages.append(package)
        for package_name in self.packager.packages['js']:
            package = self.packager.package_for('js', package_name)
            if package.manifest:
                packages.append(package)
        return packages

    def cache(self):
        ignore_patterns = getattr(settings, "STATICFILES_IGNORE_PATTERNS",
                                  None)

        if settings.PIPELINE_ENABLED:
            for package in self.packages:
                if self.pcs:
                    filename = self.pcs.hashed_name(package.output_filename)
                else:
                    filename = package.output_filename
                self.package_files.append(filename)
                yield str(self.packager.individual_url(filename))
        else:
            for package in self.packages:
                for path in self.packager.compile(package.paths):
                    self.package_files.append(path)
                    yield str(self.packager.individual_url(path))

        for finder in self.finders:
            for path, storage in finder.list(ignore_patterns):
                # Prefix the relative path if the source storage contains it
                if getattr(storage, 'prefix', None):
                    prefixed_path = os.path.join(storage.prefix, path)
                else:
                    prefixed_path = path

                # Dont add any doubles
                if prefixed_path not in self.package_files:
                    self.package_files.append(prefixed_path)
                    yield str(self.packager.individual_url(prefixed_path))
