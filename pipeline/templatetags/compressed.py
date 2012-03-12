try:
    from staticfiles.storage import staticfiles_storage
except ImportError:
    from django.contrib.staticfiles.storage import staticfiles_storage # noqa

from django import template
from django.template.loader import render_to_string

from pipeline.conf import settings
from pipeline.packager import Packager, PackageNotFound
from pipeline.utils import guess_type

register = template.Library()


class CompressedCSSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        package_name = template.Variable(self.name).resolve(context)
        package = settings.PIPELINE_CSS.get(package_name, {})
        if package:
            package = {package_name: package}
        self.packager = Packager(css_packages=package, js_packages={})

        try:
            package = self.packager.package_for('css', package_name)
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified

        if settings.PIPELINE:
            return self.render_css(package, package.output_filename)
        else:
            paths = self.packager.compile(package.paths)
            return self.render_individual(package, paths)

    def render_css(self, package, path):
        template_name = package.template_name or "pipeline/css.html"
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/css'),
            'url': staticfiles_storage.url(path)
        })
        return render_to_string(template_name, context)

    def render_individual(self, package, paths):
        tags = [self.render_css(package, path) for path in paths]
        return '\n'.join(tags)


class CompressedJSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        package_name = template.Variable(self.name).resolve(context)
        package = settings.PIPELINE_JS.get(package_name, {})
        if package:
            package = {package_name: package}
        self.packager = Packager(css_packages={}, js_packages=package)

        try:
            package = self.packager.package_for('js', package_name)
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified

        if settings.PIPELINE:
            return self.render_js(package, package.output_filename)
        else:
            paths = self.packager.compile(package.paths)
            templates = self.packager.pack_templates(package)
            return self.render_individual(package, paths, templates)

    def render_js(self, package, path):
        template_name = package.template_name or "pipeline/js.html"
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/javascript'),
            'url': staticfiles_storage.url(path)
        })
        return render_to_string(template_name, context)

    def render_inline(self, package, js):
        context = package.extra_context
        context.update({
            'source': js
        })
        return render_to_string("pipeline/inline_js.html", context)

    def render_individual(self, package, paths, templates=None):
        tags = [self.render_js(package, js) for js in paths]
        if templates:
            tags.append(self.render_inline(package, templates))
        return '\n'.join(tags)


def compressed_css(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the PIPELINE_CSS setting' % token.split_contents()[0]
    return CompressedCSSNode(name)
compressed_css = register.tag(compressed_css)


def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the PIPELINE_JS setting' % token.split_contents()[0]
    return CompressedJSNode(name)
compressed_js = register.tag(compressed_js)
