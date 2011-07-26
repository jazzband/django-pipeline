import os

from manifesto import Manifest

from pipeline.packager import Packager


class PipelineManifest(Manifest):
    def __init__(self):
        self.packager = Packager()

    def cache(self):
        packages, cache = [], []
        for package_name in self.packager.packages['css']:
            packages.append(self.packager.package_for('css', package_name))
        for package_name in self.packager.packages['js']:
            packages.append(self.packager.package_for('js', package_name))
        for package in packages:
            filename_base, filename = os.path.split(package['output'])
            version = self.packager.versioning.version_from_file(filename_base, filename)
            output_filename = self.packager.versioning.output_filename(package['output'], version)
            cache.append(str(self.packager.individual_url(output_filename)))
        return cache
