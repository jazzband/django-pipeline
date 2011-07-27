import os

from django.conf import settings

from manifesto import Manifest

from pipeline.packager import Packager


class PipelineManifest(Manifest):
    def __init__(self):
        self.packager = Packager()
        self.packages = self.collect_packages()

    def collect_packages(self):
        packages = []
        for package_name in self.packager.packages['css']:
            package = self.packager.package_for('css', package_name)
            if package['manifest']:
                packages.append(package)
        for package_name in self.packager.packages['js']:
            package = self.packager.package_for('js', package_name)
            if package['manifest']:
                packages.append(package)
        return packages

    def cache(self):
        if settings.PIPELINE:
            for package in self.packages:
                filename_base, filename = os.path.split(package['output'])
                version = self.packager.versioning.version_from_file(filename_base, filename)
                output_filename = self.packager.versioning.output_filename(package['output'], version)
                yield str(self.packager.individual_url(output_filename))
        else:
            for package in self.packages:
                for path in self.packager.compile(package['paths']):
                    yield str(self.packager.individual_url(path))

    def revision(self):
        versions = []
        if settings.PIPELINE:
            for package in self.packages:
                filename_base, filename = os.path.split(package['output'])
                version = self.packager.versioning.version_from_file(filename_base, filename)
                versions.append(str(version))
        else:
            for package in self.packages:
                version = self.packager.versioning.version(package['paths'])
                versions.append(str(version))
        versions.sort()
        return versions[-1]
