import os
import urlparse

from django.core.files.base import ContentFile
from django.utils.encoding import smart_str

from pipeline.conf import settings
from pipeline.compilers import Compiler
from pipeline.compressors import Compressor
from pipeline.glob import glob
from pipeline.signals import css_compressed, js_compressed
from pipeline.storage import storage
from pipeline.utils import filepath_to_uri
from pipeline.versioning import Versioning


class Packager(object):
    def __init__(self, verbose=False, css_packages=None, js_packages=None):
        self.verbose = verbose
        self.compressor = Compressor(verbose)
        self.versioning = Versioning(verbose)
        self.compiler = Compiler(verbose)
        if css_packages is None:
            css_packages = settings.PIPELINE_CSS
        if js_packages is None:
            js_packages = settings.PIPELINE_JS
        self.packages = {
            'css': self.create_packages(css_packages),
            'js': self.create_packages(js_packages),
        }

    def package_for(self, kind, package_name):
        try:
            return self.packages[kind][package_name].copy()
        except KeyError:
            raise PackageNotFound(
                "No corresponding package for %s package name : %s" % (
                    kind, package_name
                )
            )

    def individual_url(self, filename):
        relative_path = self.compressor.relative_path(filename)[1:]
        return urlparse.urljoin(settings.PIPELINE_URL,
            filepath_to_uri(relative_path))

    def pack_stylesheets(self, package, **kwargs):
        variant = package.get('variant', None)
        absolute_asset_paths = package.get('absolute_asset_paths', True)
        return self.pack(package, self.compressor.compress_css, css_compressed,
            variant=variant, absolute_asset_paths=absolute_asset_paths,
            **kwargs)

    def compile(self, paths):
        return self.compiler.compile(paths)

    def pack(self, package, compress, signal, sync=False, force=False, **kwargs):
        if settings.PIPELINE_AUTO or (force and sync):
            need_update, version = self.versioning.need_update(
                package['output'], package['paths'])
            if need_update or force:
                output_filename = self.versioning.output_filename(
                    package['output'],
                    version
                )
                self.versioning.cleanup(package['output'])
                if self.verbose:
                    print "Version: %s" % version
                    print "Saving: %s" % output_filename
                paths = self.compile(package['paths'])
                content = compress(paths,
                    asset_url=self.individual_url(output_filename), **kwargs)
                self.save_file(output_filename, content)
        else:
            filename_base, filename = os.path.split(package['output'])
            version = self.versioning.version_from_file(filename_base, filename, force=force)
        signal.send(sender=self, package=package, version=version, **kwargs)
        return self.versioning.output_filename(package['output'], version)

    def pack_javascripts(self, package, **kwargs):
        if 'externals' in package:
            return
        return self.pack(package, self.compressor.compress_js, js_compressed, templates=package['templates'], **kwargs)

    def pack_templates(self, package):
        return self.compressor.compile_templates(package['templates'])

    def save_file(self, path, content):
        return storage.save(path, ContentFile(smart_str(content)))

    def create_packages(self, config):
        packages = {}
        if not config:
            return packages
        for name in config:
            packages[name] = {}
            if 'external_urls' in config[name]:
                packages[name]['externals'] = config[name]['external_urls']
                continue
            paths = []
            for pattern in config[name]['source_filenames']:
                for path in glob(pattern):
                    if not path in paths:
                        paths.append(str(path))
            packages[name]['paths'] = [path for path in paths if not path.endswith(settings.PIPELINE_TEMPLATE_EXT)]
            packages[name]['templates'] = [path for path in paths if path.endswith(settings.PIPELINE_TEMPLATE_EXT)]
            packages[name]['output'] = config[name]['output_filename']
            packages[name]['context'] = {}
            packages[name]['manifest'] = True
            if 'absolute_asset_paths' in config[name]:
                packages[name]['absolute_asset_paths'] = \
                    config[name]['absolute_asset_paths']
            if 'extra_context' in config[name]:
                packages[name]['context'] = config[name]['extra_context']
            if 'template_name' in config[name]:
                packages[name]['template'] = config[name]['template_name']
            if 'variant' in config[name]:
                packages[name]['variant'] = config[name]['variant']
            if 'manifest' in config[name]:
                packages[name]['manifest'] = config[name]['manifest']
        return packages


class PackageNotFound(Exception):
    pass
