try:
    from staticfiles.finders import DefaultStorageFinder
except ImportError:
    from django.contrib.staticfiles.finders import DefaultStorageFinder # noqa

from django.conf import settings

from manifesto import Manifest

from pipeline.packager import Packager


class PipelineManifest(Manifest):
    def __init__(self):
        self.packager = Packager()
        self.packages = self.collect_packages()
        self.finder = DefaultStorageFinder()

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
        
        if settings.PIPELINE:
            for package in self.packages:
                yield str(self.packager.individual_url(package.output_filename))
        else:
            for package in self.packages:
                for path in self.packager.compile(package.paths):
                    yield str(self.packager.individual_url(path))
        for path, _ in self.finder.list(ignore_patterns):
            yield str(self.packager.individual_url(path))
