from django import template
from django.template.loader import render_to_string

from compress.conf import settings
from compress.packager import Packager, PackageNotFound

register = template.Library()


class CompressedCSSNode(template.Node):
    def __init__(self, name):
        self.name = name
        self.packager = Packager()

    def render(self, context):
        package_name = template.Variable(self.name).resolve(context)
        try:
            package = self.packager.package_for('css', package_name)
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified

        if settings.COMPRESS:
            compressed_path = self.packager.pack_stylesheets(package)
            return self.render_css(package, compressed_path)
        else:
            return self.render_individual(package)

    def render_css(self, package, path):
        context = {}
        if not 'template' in package:
            package['template'] = "compress/css.html"
        if not 'context' in package:
            context = package['context']
        context.update({
            'url': self.packager.individual_url(path)
        })
        return render_to_string(package['template'], context)

    def render_individual(self, package):
        tags = [self.render_css(package, path) for path in package['paths']]
        return '\n'.join(tags)


class CompressedJSNode(template.Node):
    def __init__(self, name):
        self.name = name
        self.packager = Packager()

    def render(self, context):
        package_name = template.Variable(self.name).resolve(context)
        try:
            package = self.packager.package_for('js', package_name)
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified

        if 'externals' in package:
            return '\n'.joins([self.render_external(package, url) for url in package['externals']])

        if settings.COMPRESS:
            compressed_path = self.packager.pack_javascripts(package)
            return self.render_js(package, compressed_path)
        else:
            return self.render_individual(package)

    def render_js(self, package, path):
        context = {}
        if not 'template' in package:
            package['template'] = "compress/js.html"
        if not 'context' in package:
            context = package['context']
        context.update({
            'url': self.packager.individual_url(path)
        })
        return render_to_string(package['template'], context)

    def render_external(self, package, url):
        if not 'template' in package:
            package['template'] = "compress/js.html"
        return render_to_string(package['template'], {
            'url': url
        })

    def render_individual(self, package):
        tags = [self.render_js(package, js) for js in package['paths']]
        return '\n'.join(tags)


def compressed_css(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the COMPRESS_CSS setting' % token.split_contents()[0]

    return CompressedCSSNode(name)
compressed_css = register.tag(compressed_css)


def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the COMPRESS_JS setting' % token.split_contents()[0]
    return CompressedJSNode(name)
compressed_js = register.tag(compressed_js)
