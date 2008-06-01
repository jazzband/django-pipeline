import os

from django.utils.http import urlquote

from django import template

from django.conf import settings as django_settings

from compress.conf import settings
from compress.utils import media_root, needs_update, filter_css, filter_js

register = template.Library()

def render_common(template_name, obj, filename):
    
    url = django_settings.MEDIA_URL + urlquote(filename)

    if settings.COMPRESS and obj.get('bump_filename', False):
        try:
            url += '?%d' % os.stat(media_root(filename)).st_mtime
        except:
             # do not output specified file if stat() fails
             # the URL could be cached forever at the client
             # this will (probably) make the problem visible, while not aborting the entire rendering
            return ''

    context = obj.get('extra_context', {})
    context['url'] = url

    return template.loader.render_to_string(template_name, context)

def render_css(css, filename):
    return render_common(css.get('template_name', 'compress/css.html'), css, filename)

def render_js(js, filename):
    return render_common(js.get('template_name', 'compress/js.html'), js, filename)

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

            if settings.COMPRESS_AUTO_TEMPLATES and needs_update(css['output_filename'], css['source_filenames']):
                filter_css(css)

            return render_css(css, css['output_filename'])
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

            if settings.COMPRESS_AUTO_TEMPLATES and needs_update(js['output_filename'], js['source_filenames']):
                filter_js(js)

            return render_js(js, js['output_filename'])
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
