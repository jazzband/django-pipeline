from __future__ import unicode_literals

from jinja2 import nodes
from jinja2.ext import Extension

from django.contrib.staticfiles.storage import staticfiles_storage

from pipeline.conf import settings
from pipeline.packager import Packager, PackageNotFound
from pipeline.utils import guess_type


class PipelineExtension(Extension):
    tags = set(['compressed_css', 'compressed_js'])

    def parse(self, parser):
        stream = parser.stream
        tag = stream.next()
        if stream.current.test('string'):
            if stream.look().test('string'):
                token = stream.next()
                package_name = token.value
            else:
                package_name = parser.parse_expression().value

        if tag.value == "compressed_css":
            return self.package_css(package_name)

        if tag.value == "compressed_js":
            return nodes.Output([
                self.call_method('package_js', args=[package_name]),
            ]).set_lineno(tag.lineno)

        return []

    def package_css(self, package_name):
        package = settings.PIPELINE_CSS.get(package_name, {})
        if package:
            package = {package_name: package}
        packager = Packager(css_packages=package, js_packages={})

        try:
            package = packager.package_for('css', package_name)
        except PackageNotFound:
            return self.environment.get_template('pipeline/css.jinja').module
            return nodes.Markup('')

        if settings.PIPELINE:
            return nodes.Markup(self.render_css(package, package.output_filename))
        else:
            paths = packager.compile(package.paths)
            return nodes.Markup(self.render_individual_css(package, paths))

    def render_css(self, package, path):
        template_name = "pipeline/css.jinja"
        if package.template_name:
            template_name = package.template_name

        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/css'),
            'url': staticfiles_storage.url(path)
        })

        template = self.environment.get_template(template_name)
        return template.render(**context)

    def render_individual_css(self, package, paths):
        tags = [self.render_css(package, path) for path in paths]
        return '\n'.join(tags)

    def package_js(self, package_name):
        return
