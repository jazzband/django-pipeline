import os

from django import template

from django.conf import settings as django_settings

from compress.conf import settings
from compress.utils import media_root

register = template.Library()

def render_common(template_name, obj, filename):
    if 'extra_context' in obj:
        context = obj['extra_context']
    else:
        context = {}
    
    url = django_settings.MEDIA_URL + filename
    if settings.COMPRESS and 'bump_filename' in obj and obj['bump_filename']:
        url += '?%d' % os.stat(media_root(filename)).st_mtime

    context.update(url=url)
    return template.loader.render_to_string(template_name, context)

def render_css(css, filename):
    return render_common('compress/css.html', css, filename)

def render_js(js, filename):
    return render_common('compress/js.html', js, filename)

class CompressedCSSNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        css_name = template.Variable(self.name).resolve(context)
        css = settings.COMPRESS_CSS[css_name]

        if settings.COMPRESS:
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
        js = settings.COMPRESS_JS[js_name]
        if settings.COMPRESS:
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
        raise template.TemplateSyntaxError, '%r requires exactly one argument, being the name of the COMPRESS_CSS setting'

    return CompressedCSSNode(name)
compressed_css = register.tag(compressed_css)

#@register.tag
def compressed_js(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r requires exactly one argument, being the name of the COMPRESS_JS setting'

    return CompressedJSNode(name)
compressed_js = register.tag(compressed_js)