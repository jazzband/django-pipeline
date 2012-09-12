try:
    from staticfiles.finders import get_finders
except ImportError:
    from django.contrib.staticfiles.finders import get_finders # noqa

import os

from django.conf import settings
from pipeline.conf.settings import (PIPELINE)

from manifesto import Manifest

from pipeline.packager import Packager


class PipelineManifest(Manifest):
    def __init__(self):
        self.packager = Packager()
        self.packages = self.collect_packages()
        self.finders = get_finders()
        self.package_files = self.get_package_files()

    def get_package_files(self):
        files = list()
        for package in self.packages:
            files.append(package.output_filename)
            for path in self.packager.compile(package.paths):
                files.append(path)

        return files     

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
        ignore_patterns = getattr(settings, "STATICFILES_IGNORE_PATTERNS", None)
        
        if PIPELINE:
            for package in self.packages:
                yield str(self.packager.individual_url(package.output_filename))
        else:
            for package in self.packages:
                for path in self.packager.compile(package.paths):
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
                    yield str(self.packager.individual_url(prefixed_path))
