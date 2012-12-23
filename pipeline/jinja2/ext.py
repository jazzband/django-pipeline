try:
    from staticfiles.storage import staticfiles_storage
except ImportError:
    from django.contrib.staticfiles.storage import staticfiles_storage  # noqa

from jinja2 import nodes
from jinja2.ext import Extension

from pipeline.conf import settings
from pipeline.packager import Packager, PackageNotFound


class PipelineExtension(Extension):
    tags = set(['compressed_css', 'compressed_js'])

    def parse(self, parser):
        stream = parser.stream
        tag = stream.next()
        if stream.current.test('string'):
            if stream.look().test('string'):
                token = stream.next()
                package_name = nodes.Const(token.value, lineno=token.lineno)
            else:
                package_name = parser.parse_expression()

        if tag.value == "compressed_css":
            return self.package_css(package_name)

        if tag.value == "compressed_js":
            return self.package_js(package_name)

        return []

    def package_css(self, package_name):
        package = settings.PIPELINE_CSS.get(package_name, {})
        if package:
            package = {package_name: package}
        packager = Packager(css_packages=package, js_packages={})

        try:
            package = packager.package_for('css', package_name)
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified

        if settings.PIPELINE:
            return self.render_css(package, package.output_filename)
        else:
            paths = packager.compile(package.paths)
            return self.render_individual(package, paths)

    def render_css(self, package, path):
        print "render"
        return

    def render_individual(self, package, paths):
        print "render"
        return

    def package_js(self, package_name):
        return
