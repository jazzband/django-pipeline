from __future__ import unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage

from django import template
from django.template.base import VariableDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from ..collector import default_collector
from ..conf import settings
from ..packager import Packager, PackageNotFound
from ..utils import guess_type
import os


register = template.Library()


class PipelineMixin(object):
    request = None
    _request_var = None

    @property
    def request_var(self):
        if not self._request_var:
            self._request_var = template.Variable('request')
        return self._request_var

    def package_for(self, package_name, package_type):
        package = {
            'js': getattr(settings, 'PIPELINE_JS', {}).get(package_name, {}),
            'css': getattr(settings, 'PIPELINE_CSS', {}).get(package_name, {}),
        }[package_type]

        if package:
            package = {package_name: package}

        packager = {
            'js': Packager(css_packages={}, js_packages=package),
            'css': Packager(css_packages=package, js_packages={}),
        }[package_type]

        return packager.package_for(package_type, package_name)

    def render(self, context):
        try:
            self.request = self.request_var.resolve(context)
        except VariableDoesNotExist:
            pass

    def render_compressed(self, package, package_type):
        if settings.PIPELINE_ENABLED:
            method = getattr(self, "render_{0}".format(package_type))
            return method(package, package.output_filename)
        else:
            default_collector.collect(self.request)

            packager = Packager()
            method = getattr(self, "render_individual_{0}".format(package_type))
            paths = packager.compile(package.paths)
            templates = packager.pack_templates(package)
            return method(package, paths, templates=templates)


class StylesheetNode(PipelineMixin, template.Node):
    def __init__(self, name, inline):
        self.name = name
        self.inline = inline

    def render(self, context):
        super(StylesheetNode, self).render(context)
        package_name = template.Variable(self.name).resolve(context)

        try:
            package = self.package_for(package_name, 'css')
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified
        return self.render_compressed(package, 'css')

    def render_css(self, package, path):
        if self.inline == 'inline':
            data = ""
            with open (os.getcwd()+"/static/"+path, "r") as myfile:
                data=myfile.read()
            if data != "":
                return self.render_inline(package=package, css=data)
        template_name = package.template_name or "pipeline/css.html"
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/css'),
            'url': mark_safe(staticfiles_storage.url(path))
        })
        return render_to_string(template_name, context)

    def render_inline(self, package, css):
        context = package.extra_context
        context.update({
            'source': css
        })
        return render_to_string("pipeline/inline_css.html", context)

    def render_individual_css(self, package, paths, **kwargs):
        tags = [self.render_css(package, path) for path in paths]
        return '\n'.join(tags)


class JavascriptNode(PipelineMixin, template.Node):
    def __init__(self, name, inline):
        self.name = name
        self.inline = inline

    def render(self, context):
        super(JavascriptNode, self).render(context)
        package_name = template.Variable(self.name).resolve(context)

        try:
            package = self.package_for(package_name, 'js')
        except PackageNotFound:
            return ''  # fail silently, do not return anything if an invalid group is specified
        return self.render_compressed(package, 'js')

    def render_js(self, package, path):
        if self.inline == 'inline':
            data = ""
            with open (os.getcwd()+"/static/"+path, "r") as myfile:
                data=myfile.read()
            if data != "":
                return self.render_inline(package=package, js=data)
        template_name = package.template_name or "pipeline/js.html"
        context = package.extra_context
        context.update({
            'type': guess_type(path, 'text/javascript'),
            'url': mark_safe(staticfiles_storage.url(path))
        })
        return render_to_string(template_name, context)

    def render_inline(self, package, js):
        context = package.extra_context
        context.update({
            'source': js
        })
        return render_to_string("pipeline/inline_js.html", context)

    def render_individual_js(self, package, paths, templates=None):
        tags = [self.render_js(package, js) for js in paths]
        if templates:
            tags.append(self.render_inline(package, templates))
        return '\n'.join(tags)



@register.tag
def stylesheet(parser, token):
    inline = ""
    try:
        try:
            tag_name, name, inline = token.split_contents()
        except ValueError:
            tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r requires exactly one argument: the name of a group in the PIPELINE_CSS setting' % token.split_contents()[0])
    return StylesheetNode(name, inline)


@register.tag
def javascript(parser, token):
    inline = ""
    try:
        try:
            tag_name, name, inline = token.split_contents()
        except ValueError:
            tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%r requires exactly one argument: the name of a group in the PIPELINE_JS setting' % token.split_contents()[0])
    return JavascriptNode(name, inline)
