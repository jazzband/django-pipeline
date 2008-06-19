import os

from django import template

from django.conf import settings as django_settings

from compress.conf import settings
from compress.utils import media_root, media_url, needs_update, filter_css, filter_js, get_output_filename, get_version

register = template.Library()

def render_common(template_name, obj, filename, version):
    if settings.COMPRESS:
        filename = get_output_filename(filename, get_version(version))

    context = obj.get('extra_context', {})
    context['url'] = media_url(filename)

    return template.loader.render_to_string(template_name, context)

def render_css(css, filename, version=None):
    return render_common(css.get('template_name', 'compress/css.html'), css, filename, version)

def render_js(js, filename, version=None):
    return render_common(js.get('template_name', 'compress/js.html'), js, filename, version)

class CompressedCSSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        css_name = template.Variable(self.name).resolve(context)

        try:
            css = settings.COMPRESS_CSS[css_name]
        except KeyError:
            return '' # fail silently, do not return anything if an invalid group is specified

        if settings.COMPRESS:

            if settings.COMPRESS:

                version = None

                if settings.COMPRESS_AUTO:
                    u, version = needs_update(css['output_filename'], css['source_filenames'])
                    if u:
                        filter_css(css)

            return render_css(css, css['output_filename'], version)
        else:
            # output source files
            r = ''
            for source_file in css['source_filenames']:
                r += render_css(css, source_file)

            return r

class CompressedJSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        js_name = template.Variable(self.name).resolve(context)

        try:
            js = settings.COMPRESS_JS[js_name]
        except KeyError:
            return '' # fail silently, do not return anything if an invalid group is specified

        if settings.COMPRESS:

            version = None

            if settings.COMPRESS_AUTO:
                u, version = needs_update(js['output_filename'], js['source_filenames'])
                if u:
                    filter_js(js)

            return render_js(js, js['output_filename'], version)
        else:
            # output source files
            r = ''
            for source_file in js['source_filenames']:
                r += render_js(js, source_file)
            return r

#@register.tag
def compressed_css(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the COMPRESS_CSS setting' % token.split_contents()[0]

    return CompressedCSSNode(name)
compressed_css = register.tag(compressed_css)

#@register.tag
def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument: the name of a group in the COMPRESS_JS setting' % token.split_contents()[0]

    return CompressedJSNode(name)
compressed_js = register.tag(compressed_js)
